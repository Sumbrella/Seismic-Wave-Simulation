from abc import ABC, abstractmethod
import numpy as np

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
        self.rho = None
        self.required_c = ["rho", "c11", "c44"]
        self.vpmax = None
        self.vsmax = None

        self.rho = None
        self.c11 = None
        self.c12 = None
        self.c44 = None

    @abstractmethod
    def load_file(self, *args):
        pass

    @abstractmethod
    def init_by_val(self, *args):
        pass

    @abstractmethod
    def calculate_step_value(self, ux, uz, use_anti_extension=False, method='psm'):
        pass

    def check_speed(self):
        self.vpmax = np.max(np.sqrt(self.c11 / self.rho))
        self.vsmax = np.max(np.sqrt(self.c44 / self.rho))

        print("Max P velocity of this medium is: {:.3f}".format(self.vpmax))
        print("Max S velocity of this medium is: {:.3f}".format(self.vsmax))

    def _set_required_by_kwargs(self, **kwargs):
        for c_attr in self.required_c:
            if not hasattr(self, c_attr):
                AttributeError(f"Error: medium need {c_attr} matrix member, but input don't provide.")
            print(f"Setting {c_attr}, value: {kwargs.get(c_attr)}")
            setattr(self, c_attr, kwargs.get(c_attr))

    def _check_c_shape(self, c: np.ndarray, cname: str):
        assert len(c.shape) == 2, f"Input {cname} dimension is {len(c.shape)}, not 2D."
        assert c.shape == self.cfg.shape, f"Input {cname} shape is {c.shape} not match the medium shape {self.cfg.shape}"

    def _check_required_c_shape(self):
        self._check_c_shape(self.rho, 'rho')
        for c_attr in self.required_c:
            self._check_c_shape(getattr(self, c_attr), c_attr)


class IMedium(Medium):
    def __init__(self, cfg: MediumConfig, *arg, **kwargs):
        super(IMedium, self).__init__(cfg, *arg, **kwargs)
        self.c11 = None
        self.c12 = None
        self.c44 = None
        self.required_c.append("c12")

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
        self._set_required_by_kwargs(
            rho=rho,
            c11=c11,
            c12=c12,
            c44=(c11 - c12) / 2
        )
        self._check_required_c_shape()
        self.check_speed()

    def calculate_step_value(self, ux, uz, use_anti_extension=False, method='psm'):
        if not use_anti_extension:
            from tools.psm import cal_dx, cal_dz, cal_ddx, cal_ddz
            return np.asarray(
                [
                    self.c11 * cal_ddx(ux, self.cfg.kx) +
                    (self.c12 + self.c44) * cal_dz(cal_dx(uz, self.cfg.kx), self.cfg.kz) +
                    self.c44 * cal_ddz(ux, self.cfg.kz),
                    self.c11 * cal_ddz(uz, self.cfg.kz) +
                    (self.c12 + self.c44) * cal_dz(cal_dx(ux, self.cfg.kx), self.cfg.kz) +
                    self.c44 * cal_ddx(uz, self.cfg.kx)
                ]
            )
        else:
            from tools.psm_anti import cal_dx, cal_dz, cal_ddx, cal_ddz
            return np.asarray(
                [
                    self.c11 * cal_ddx(ux, self.cfg.kx2) +
                    (self.c12 + self.c44) * cal_dz(cal_dx(uz, self.cfg.kx2), self.cfg.kz2) +
                    self.c44 * cal_ddz(ux, self.cfg.kz2),
                    self.c11 * cal_ddz(uz, self.cfg.kz2) +
                    (self.c12 + self.c44) * cal_dz(cal_dx(ux, self.cfg.kx2), self.cfg.kz2) +
                    self.c44 * cal_ddx(uz, self.cfg.kx2)
                ]
            )


class VTIMedium(Medium):
    def __init__(self, cfg: MediumConfig, *args, **kwargs):
        super().__init__(cfg, *args, **kwargs)
        self.required_c.append("c33")
        self.c33 = None
        self.required_c.append("c12")
        self.c12 = None
        print(self.required_c)

    def load_file(self):
        pass  # TODO

    def init_by_val(self, rho, c11, c12, c33, c44):
        self._set_required_by_kwargs(
            rho=rho,
            c11=c11,
            c12=c12,
            c33=c33,
            c44=c44
        )
        self._check_required_c_shape()
        self.check_speed()

    def calculate_step_value(self, ux, uz, use_anti_extension=False, method='psm'):
        if not use_anti_extension:
            from tools.psm import cal_dx, cal_dz, cal_ddx, cal_ddz
            return np.array([
                self.c11 * cal_ddx(ux, self.cfg.kx) +
                self.c44 * cal_ddz(ux, self.cfg.kz) +
                (self.c12 + self.c44) * cal_dx(cal_dz(uz, self.cfg.kz), self.cfg.kx),
                (self.c44 + self.c12) * cal_dz(cal_dx(ux, self.cfg.kx), self.cfg.kz) +
                self.c44 * cal_ddx(uz, self.cfg.kx) +
                self.c33 * cal_ddz(uz, self.cfg.kz)
            ])
        else:
            from tools.psm_anti import cal_dx, cal_dz, cal_ddx, cal_ddz
            return np.array([
                self.c11 * cal_ddx(ux, self.cfg.kx2) +
                self.c44 * cal_ddz(ux, self.cfg.kz2) +
                (self.c12 + self.c44) * cal_dx(cal_dz(uz, self.cfg.kz2), self.cfg.kx2),
                (self.c44 + self.c12) * cal_dz(cal_dx(ux, self.cfg.kx2), self.cfg.kz2) +
                self.c44 * cal_ddx(uz, self.cfg.kx2) +
                self.c33 * cal_ddz(uz, self.cfg.kz2)
            ])


class HTIMedium(Medium):
    def __init__(self, cfg: MediumConfig, *args, **kwargs):
        super().__init__(cfg, *args, **kwargs)
        self.required_c.append("c12")
        self.c12 = None
        self.required_c.append("c33")
        self.c33 = None
        self.required_c.append("c55")
        self.c55 = None

    def load_file(self):
        pass  # TODO

    def init_by_val(self, rho, c11, c12, c33, c55):
        self._set_required_by_kwargs(
            rho=rho,
            c11=c11,
            c12=c12,
            c33=c33,
            c44=(c11 - c12) / 2,
            c55=c55
        )
        self._check_required_c_shape()
        self.check_speed()

    def calculate_step_value(self, ux, uz, use_anti_extension=False, method='psm'):
        if not use_anti_extension:
            from tools.psm import cal_dx, cal_dz, cal_ddx, cal_ddz
            return np.array([
                self.c11 * cal_ddx(ux, self.cfg.kx) +
                self.c55 * cal_ddz(ux, self.cfg.kz) +
                (self.c12 + self.c55) * cal_dx(cal_dz(uz, self.cfg.kz), self.cfg.kx),
                self.c55 * cal_ddx(uz, self.cfg.kx) +
                (self.c12 + self.c55) * cal_dx(cal_dz(ux, self.cfg.kz), self.cfg.kx) +
                self.c33 * cal_ddz(uz, self.cfg.kz)
            ])
        else:
            from tools.psm_anti import cal_dx, cal_dz, cal_ddx, cal_ddz
            return np.array([
                self.c11 * cal_ddx(ux, self.cfg.kx2) +
                self.c55 * cal_ddz(ux, self.cfg.kz2) +
                (self.c12 + self.c55) * cal_dx(cal_dz(uz, self.cfg.kz2), self.cfg.kx2),
                self.c55 * cal_ddx(uz, self.cfg.kx2) +
                (self.c12 + self.c55) * cal_dx(cal_dz(ux, self.cfg.kz2), self.cfg.kx2) +
                self.c33 * cal_ddz(uz, self.cfg.kz2)
            ])
