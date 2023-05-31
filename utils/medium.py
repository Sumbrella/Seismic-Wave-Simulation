import os
from abc import ABC, abstractmethod

from tools.psm import *
from tools import check_file_exists, get_file_ext
from .medium_config import MediumConfig


class Medium(ABC):
    @classmethod
    def get_medium(cls, cfg: MediumConfig):
        if cfg.medium_type == 'I':
            return IMedium(cfg)
        elif cfg.medium_type == 'VTI':
            return VTIMedium(cfg)
        elif cfg.medium_type == 'HTI':
            return HTIMedium(cfg)
        else:
            ValueError("medium type does not support.")

    def __init__(self, cfg: MediumConfig, *args, **kwargs):
        self.cfg = cfg
        self.rho = []
        self.required_c = []
        self.vpmax = None
        self.vsmax = None
        self.c11 = None
        self.c44 = None

    @abstractmethod
    def load_file(self, *args):
        pass

    @abstractmethod
    def init_by_val(self, *args):
        pass

    @abstractmethod
    def calculate_step_value(self, ux, uz, method='psm'):
        pass

    def check_speed(self):
        self.vpmax = np.max(np.sqrt(self.c11 / self.rho))
        self.vsmax = np.max(np.sqrt(self.c44 / self.rho))

        print("Max P veclocity of this medium is: {:.3f}".format(self.vpmax))
        print("Max S veclocity of this medium is: {:.3f}".format(self.vsmax))

    def _check_c_shape(self, c: np.ndarray, cname: str):
        assert len(c.shape) == 2, f"Input {cname} dimension is {len(c.shape)}, not 2D."
        assert c.shape == self.cfg.shape, f"Input {cname} shape is {c.shape} not match the medium shape {self.cfg.shape}"


class IMedium(Medium):
    def __init__(self, cfg: MediumConfig, *arg, **kwargs):
        super(IMedium, self).__init__(cfg, *arg, **kwargs)
        self.c11 = None
        self.c12 = None
        self.c44 = None
        self.required_c = ["c11", "c12"]

    def load_file(self, rho_file: str, c11_file: str, c12_file: str, *args):
        check_file_exists(c11_file)
        check_file_exists(c12_file)
        check_file_exists(rho_file)

        cs = []
        for file in [rho_file, c11_file, c12_file]:
            ext = get_file_ext(file)
            if ext == '.txt':
                c = np.loadtxt(file)
            elif ext == '.npy':
                c = np.load(file)
            else:
                TypeError(f"file extension {ext} don't support. ")
                break
            cs.append(c)

        rho, c11, c12 = cs
        self.init_by_val(rho, c11, c12)

    def init_by_val(self, rho, c11, c12):
        # C11 = \lambda + 2\mu   C12 = \lambda  C44 = \mu
        rho = np.asarray(rho)
        c11 = np.asarray(c11)
        c12 = np.asarray(c12)

        self._check_c_shape(rho, "rho")
        self._check_c_shape(c11, "C11")
        self._check_c_shape(c12, "C12")

        self.rho = rho
        self.c11 = c11
        self.c12 = c12
        self.c44 = (self.c11 - self.c12) / 2

        self.check_speed()

    def calculate_step_value(self, ux, uz, method='psm'):
        return np.asarray(
            [
                self.c11 * cal_psm_ddx(ux, self.cfg.kx) +
                (self.c12 + self.c44) * cal_psm_dz(cal_psm_dx(uz, self.cfg.kx), self.cfg.kz) +
                self.c44 * cal_psm_ddz(ux, self.cfg.kz),
                self.c11 * cal_psm_ddz(uz, self.cfg.kz) +
                (self.c12 + self.c44) * cal_psm_dz(cal_psm_dx(ux, self.cfg.kx), self.cfg.kz) +
                self.c44 * cal_psm_ddx(uz, self.cfg.kx)
            ]
        )


class VTIMedium(Medium):
    def __init__(self, cfg: MediumConfig, *args, **kwargs):
        super().__init__(cfg, *args, **kwargs)
        self.required_c = ["c11", "c12", "c33", "c44"]

    def load_file(self):
        pass  # TODO

    def init_by_val(self, rho, c11, c12, c33, c44):
        rho = np.asarray(rho)
        c11 = np.asarray(c11)
        c12 = np.asarray(c12)
        c33 = np.asarray(c33)
        c44 = np.asarray(c44)

        self._check_c_shape(rho, "rho")
        self._check_c_shape(c11, "C11")
        self._check_c_shape(c12, "C13")
        self._check_c_shape(c33, "C33")
        self._check_c_shape(c44, "C44")

        self.rho = rho
        self.c11 = c11
        self.c12 = c12
        self.c33 = c33
        self.c44 = c44

        self.check_speed()

    def calculate_step_value(self, ux, uz, method='psm'):
        # return np.array([
        #     self.C11 * cal_psm_ddx(ux, self.cfg.kx) + 
        #     (self.C13 + self.C66) * cal_psm_dz(cal_psm_dx(uz, self.cfg.kx), self.cfg.kz) +
        #     (self.C66) * cal_psm_ddz(ux, self.cfg.kz),
        #     (self.C44 + self.C13) * cal_psm_ddx(ux, self.cfg.kx) + 
        #     self.C44 * cal_psm_ddx(uz, self.cfg.kx) + 
        #     self.C33 * cal_psm_ddz(uz, self.cfg.kz)
        # ])
        return np.array([
            self.c11 * cal_psm_ddx(ux, self.cfg.kx) + \
            self.c44 * cal_psm_ddz(ux, self.cfg.kz) + \
            (self.c12 + self.c44) * cal_psm_dx(cal_psm_dz(uz, self.cfg.kz), self.cfg.kx),
            # (self.C44 + self.C13) * cal_psm_ddx(ux, self.cfg.kx) +\
            (self.c44 + self.c12) * cal_psm_dz(cal_psm_dx(ux, self.cfg.kx), self.cfg.kz) + \
            self.c44 * cal_psm_ddx(uz, self.cfg.kx) + \
            self.c33 * cal_psm_ddz(uz, self.cfg.kz)
        ])


class HTIMedium(Medium):
    def __init__(self, cfg: MediumConfig, *args, **kwargs):
        super().__init__(cfg, *args, **kwargs)
        self.required_c = ['c11', 'c12', 'c33', 'c55']

    def load_file(self):
        pass  # TODO

    def init_by_val(self, rho, c11, c12, c33, c55):
        rho = np.asarray(rho)
        c11 = np.asarray(c11)
        c12 = np.asarray(c12)
        c33 = np.asarray(c33)
        c55 = np.asarray(c55)

        self._check_c_shape(rho, "rho")
        self._check_c_shape(c11, "C11")
        self._check_c_shape(c12, "C13")
        self._check_c_shape(c33, "C33")
        self._check_c_shape(c55, "C55")

        self.rho = rho
        self.c11 = c11
        self.c12 = c12
        self.c33 = c33
        self.c44 = (self.c11 - self.c12) / 2
        self.c55 = c55

        self.check_speed()

    def calculate_step_value(self, ux, uz, method='psm'):
        # return np.array([
        #     self.C11 * cal_psm_ddx(ux, self.cfg.kx) + 
        #     (self.C13 + self.C66) * cal_psm_dz(cal_psm_dx(uz, self.cfg.kx), self.cfg.kz) +
        #     (self.C66) * cal_psm_ddz(ux, self.cfg.kz),
        #     (self.C44 + self.C13) * cal_psm_ddx(ux, self.cfg.kx) + 
        #     self.C44 * cal_psm_ddx(uz, self.cfg.kx) + 
        #     self.C33 * cal_psm_ddz(uz, self.cfg.kz)
        # ])
        return np.array([
            self.c11 * cal_psm_ddx(ux, self.cfg.kx) +
            self.c55 * cal_psm_ddz(ux, self.cfg.kz) +
            (self.c12 + self.c55) * cal_psm_dx(cal_psm_dz(uz, self.cfg.kz), self.cfg.kx),
            self.c55 * cal_psm_ddx(uz, self.cfg.kx) +
            (self.c12 + self.c55) * cal_psm_dx(cal_psm_dz(ux, self.cfg.kz), self.cfg.kx) +
            self.c33 * cal_psm_ddz(uz, self.cfg.kz)
        ])
