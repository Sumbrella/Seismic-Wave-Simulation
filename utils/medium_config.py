import numpy as np


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

        self.kx = self.cal_kx()
        self.kz = self.cal_kz()

        self.show_parameters()

    def cal_kx(self):
        # return np.fft.fftfreq(self.nx, self.dx)
        return np.array(
            [
                i * (np.pi / self.dx) / (self.nx / 2) if i <= self.nx / 2 else
                i * (np.pi / self.dx) / (self.nx / 2) - 2 * np.pi / self.dx
                for i in range(self.nx)
            ]
        )

    def cal_kz(self):
        # return np.fft.fftfreq(self.nz, self.dz)
        return np.array(
            [
                i * (np.pi / self.dz) / (self.nz / 2) if i <= self.nz / 2 else
                i * (np.pi / self.dz) / (self.nz / 2) - 2 * np.pi / self.dz
                for i in range(self.nz)
            ]
        )

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
