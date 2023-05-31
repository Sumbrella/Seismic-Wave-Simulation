import numpy as np

class MediumConfig:
    def __init__(
            self, 
            xmin:float, xmax:float, dx:float, 
            zmin:float, zmax:float, dz:float, 
            mediumType:str # ['I', 'VTI', 'TTI']
        ):
        self.xmin = xmin
        self.xmax = xmax 
        self.dx   = dx
        self.nx   = int(np.ceil((xmax - xmin) / dx))

        self.zmin = zmin
        self.zmax = zmax
        self.dz   = dz
        self.nz   = int(np.ceil((zmax - zmin) / dx))
        
        self.mediumType = mediumType
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
        print(self.__str__)
    
    def __str__(self):
        return f"""\
--------------------------- Basic Medium Config --------------------------------
XAXIS-Range:
\txmin: {self.xmin:.3f}\txmax: {self.xmax:.3f}\tnx: {self.nx}
ZAXIS-Range:
\tzmin: {self.zmin:.3f}\tzmax: {self.zmax:.3f}\tnz: {self.nz}
--------------------------------------------------------------------------------
"""