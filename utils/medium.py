import os
from abc import ABC, abstractclassmethod

from tools.psm import *
from tools.get_file_ext import getFileExt
from utils.medium_config import MediumConfig

from .medium_config import MediumConfig


class Medium(ABC):
    @classmethod
    def getMedium(cls, cfg:MediumConfig):
        if cfg.mediumType == 'I':
            return IMedium(cfg)
        elif cfg.mediumType == 'VTI':
            return VTIMedium(cfg)
        elif cfg.mediumType == 'HTI':
            return HTIMedium(cfg)
        else:
            ValueError("medium type does not support.")
    
    def __init__(self, cfg:MediumConfig):
        self.cfg = cfg
        self.rho = []
        self.vps = []
        self.vss = []
    
    @abstractclassmethod
    def loadFile(self, filename, *args):
        pass

    @abstractclassmethod
    def initByVal(self, *args):
        pass

    @abstractclassmethod
    def initByFun(self, *args):
        pass

    @abstractclassmethod
    def calculateStepValue(self, ux, uz, method='psm'):
        pass

    def _check_file_exists(self, filename):
        assert os.path.exists(filename), f"{filename} file doesn't find."

    def _check_C_shape(self, C, Cname:str):
        assert len(C.shape) == 2, f"Input {Cname} dimension is {len(C.shape)}, not 2D."
        assert C.shape == self.cfg.shape, f"Input {Cname} shape is {C.shape} not match the medium shape {self.cfg.shape}"
    


class IMedium(Medium):
    def __init__(self, cfg:MediumConfig, *arg, **kwargs):
        super(IMedium, self).__init__(cfg, *arg, **kwargs)

    def loadFile(self, rhoFile: str, C11File:str, C12File:str, *args):
        self._check_file_exists(C11File)
        self._check_file_exists(C12File)
        self._check_file_exists(rhoFile)

        Cs = []
        for file in [rhoFile, C11File, C12File]:
            ext = getFileExt(file)
            if ext == '.txt':
                C = np.loadtxt(file)
            elif ext == '.npy':
                C = np.load(file)
            else:
                TypeError(f"file extension {ext} don't support. ")
            Cs.append(C)

        rho, C11, C12 = C
        self.initByVal(rho, C11, C12)

    def initByVal(self, rho, C11, C12): 
        # C11 = \lambda + 2\mu   C12 = \lambda  C44 = \mu
        rho = np.asarray(rho)
        C11 = np.asarray(C11)
        C12 = np.asarray(C12)

        self._check_C_shape(rho, "rho")
        self._check_C_shape(C11, "C11")
        self._check_C_shape(C12, "C12")

        self.C11 = C11
        self.C12 = C12
        self.C44 = (self.C11 - self.C12) / 2
        self.rho = rho

        self.vpmax = np.max(np.sqrt(self.C11 / self.rho))
        self.vsmax = np.max(np.sqrt(self.C44 / self.rho))

        print("Max P veclocity of this medium is: {:.3f}".format(self.vpmax))
        print("Max S veclocity of this medium is: {:.3f}".format(self.vsmax))
    
    def initByFun(self):
        pass # TODO:
    
    def calculateStepValue(self, ux, uz, method='psm'):
        return np.asarray(
            [
                self.C11 * cal_psm_ddx(ux, self.cfg.kx) +\
                (self.C12 + self.C44) * cal_psm_dz(cal_psm_dx(uz, self.cfg.kx), self.cfg.kz) +\
                self.C44 * cal_psm_ddz(ux, self.cfg.kz), 
                self.C11  * cal_psm_ddz(uz, self.cfg.kz) +\
                (self.C12 + self.C44) * cal_psm_dz(cal_psm_dx(ux, self.cfg.kx), self.cfg.kz) +\
                self.C44 * cal_psm_ddx(uz, self.cfg.kx)
            ]
        )


class VTIMedium(Medium):
    def __init__(self, cfg: MediumConfig, *args, **kwargs):
        super().__init__(cfg, *args, **kwargs)
    
    def loadFile(self):
        pass #TODO

    def initByVal(self, rho, C11, C13, C33, C44):
        rho = np.asarray(rho)
        C11 = np.asarray(C11)
        C13 = np.asarray(C13)
        C33 = np.asarray(C33)
        C44 = np.asarray(C44)

        self._check_C_shape(rho, "rho")
        self._check_C_shape(C11, "C11")
        self._check_C_shape(C13, "C13")
        self._check_C_shape(C33, "C33")
        self._check_C_shape(C44, "C44")

        self.rho = rho
        self.C11 = C11
        self.C13 = C13
        self.C33 = C33
        self.C44 = C44

        self.vpmax = np.max(np.sqrt(self.C11 / self.rho))
        self.vsmax = np.max(np.sqrt(self.C44 / self.rho))

        print("Max P veclocity of this medium is: {:.3f}".format(self.vpmax))
        print("Max S veclocity of this medium is: {:.3f}".format(self.vsmax))

    def initByFun(self):
        pass

    def calculateStepValue(self, ux, uz, method='psm'):
        # return np.array([
        #     self.C11 * cal_psm_ddx(ux, self.cfg.kx) + 
        #     (self.C13 + self.C66) * cal_psm_dz(cal_psm_dx(uz, self.cfg.kx), self.cfg.kz) +
        #     (self.C66) * cal_psm_ddz(ux, self.cfg.kz),
        #     (self.C44 + self.C13) * cal_psm_ddx(ux, self.cfg.kx) + 
        #     self.C44 * cal_psm_ddx(uz, self.cfg.kx) + 
        #     self.C33 * cal_psm_ddz(uz, self.cfg.kz)
        # ])
        return np.array([
            self.C11 * cal_psm_ddx(ux, self.cfg.kx) +\
            self.C44 * cal_psm_ddz(ux, self.cfg.kz) +\
            (self.C13 + self.C44) * cal_psm_dx(cal_psm_dz(uz, self.cfg.kz), self.cfg.kx),
            # (self.C44 + self.C13) * cal_psm_ddx(ux, self.cfg.kx) +\
            (self.C44 + self.C13) * cal_psm_dz(cal_psm_dx(ux, self.cfg.kx), self.cfg.kz) +\
            self.C44 * cal_psm_ddx(uz, self.cfg.kx) +\
            self.C33 * cal_psm_ddz(uz, self.cfg.kz)
        ])


class HTIMedium(Medium):
    def __init__(self, cfg: MediumConfig, *args, **kwargs):
        super().__init__(cfg, *args, **kwargs)
    
    def loadFile(self):
        pass #TODO

    def initByVal(self, rho, C11, C13, C33, C55):
        rho = np.asarray(rho)
        C11 = np.asarray(C11)
        C13 = np.asarray(C13)
        C33 = np.asarray(C33)
        C55 = np.asarray(C55)

        self._check_C_shape(rho, "rho")
        self._check_C_shape(C11, "C11")
        self._check_C_shape(C13, "C13")
        self._check_C_shape(C33, "C33")
        self._check_C_shape(C55, "C55")

        self.rho = rho
        self.C11 = C11
        self.C13 = C13
        self.C33 = C33
        self.C55 = C55

        # self.C44 = (self.C33 - self.C)
        self.vpmax = np.max(np.sqrt(self.C11 / self.rho))
        self.vsmax = np.max(np.sqrt(self.C55 / self.rho))

        print("Max P veclocity of this medium is: {:.3f}".format(self.vpmax))
        print("Max S veclocity of this medium is: {:.3f}".format(self.vsmax))

    def initByFun(self):
        pass

    def calculateStepValue(self, ux, uz, method='psm'):
        # return np.array([
        #     self.C11 * cal_psm_ddx(ux, self.cfg.kx) + 
        #     (self.C13 + self.C66) * cal_psm_dz(cal_psm_dx(uz, self.cfg.kx), self.cfg.kz) +
        #     (self.C66) * cal_psm_ddz(ux, self.cfg.kz),
        #     (self.C44 + self.C13) * cal_psm_ddx(ux, self.cfg.kx) + 
        #     self.C44 * cal_psm_ddx(uz, self.cfg.kx) + 
        #     self.C33 * cal_psm_ddz(uz, self.cfg.kz)
        # ])
        return np.array([
            self.C11 * cal_psm_ddx(ux, self.cfg.kx) +\
            self.C55 * cal_psm_ddz(ux, self.cfg.kz) +\
            (self.C13 + self.C55) * cal_psm_dx(cal_psm_dz(uz, self.cfg.kz), self.cfg.kx),
            self.C55 * cal_psm_ddx(uz, self.cfg.kx) +\
            (self.C13 + self.C55) * cal_psm_dx(cal_psm_dz(ux, self.cfg.kz), self.cfg.kx) +\
            self.C33 * cal_psm_ddz(uz, self.cfg.kz)
        ])