import numpy as np
from tools.psm import cal_psm_k


class MediumConfig:
    def __init__(
            self,
            xmin: float, xmax: float, dx: float,
            zmin: float, zmax: float, dz: float,
            medium_type: str  # ['I', 'VTI', 'TTI']
    ):
        self.xmin = xmin
        self.xmax = xmax
        self.dx = dx
        self.nx = int(np.ceil((xmax - xmin) / dx))

        self.zmin = zmin
        self.zmax = zmax
        self.dz = dz
        self.nz = int(np.ceil((zmax - zmin) / dx))

        self.medium_type = medium_type
        self.shape = (self.nz, self.nx)

        self.kx = cal_psm_k(self.nx, 2 * np.pi / (self.dx * self.nx))
        self.kz = cal_psm_k(self.nz, 2 * np.pi / (self.dx * self.nx))

        self.kx2 = cal_psm_k(self.nx * 2, np.pi / (self.dx * self.nx))
        self.kz2 = cal_psm_k(self.nz * 2, np.pi / (self.dz * self.nz))

        self.show_parameters()

    def show_parameters(self):
        print(self)

    def __str__(self):
        return f"""\
--------------------------- Basic Medium Config --------------------------------
XAXIS-RANGE:
\txmin: {self.xmin:.2f}m\txmax: {self.xmax:.2f}m\tnx: {self.nx}
ZAXIS-RANGE:
\tzmin: {self.zmin:.2f}m\tzmax: {self.zmax:.2f}m\tnz: {self.nz}
MEDIUM_TYPE:
\t{self.medium_type}
--------------------------------------------------------------------------------
"""
