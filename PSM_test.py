import numpy as np

class PSMSimulator:
    """simple simulator for pseudospectral method(psm) on wavefiled.
    """
    def __init__(
        self,
        xmin,
        xmax,
        zmin,
        zmax,
        endt,
        nx,
        nz,
        nt,
        fm,
        sx,
        sz,
        rho,
        lamb,
        mu
    ):
        """Initialize PSMSimulator

        Args
        --------------
            xmin (float): the min value of x-axis
            xmax (float): the max value of x-axis
            zmin (float): the min value of z-axis
            zmax (float): the max value of z-axis
            endt (float): end time
            nt (int): number of time
            nx (int): number of segments of x
            nz (int): number of segments of z
            fm (float): main frequency of source
            sx (int): source point of x-axis index
            sz (int): source point of z-axis index
            C (numpy.array): 4d array, the elastic constants, shape like (i, j, nz, nx)
        """
        self.xmin = xmin
        self.xmax = xmax
        self.zmin = zmin
        self.zmax = zmax
        self.endt = endt
        self.nt   = nt
        self.nx   = nx
        self.nz   = nz
        self.fm   = fm
        self.sx   = sx
        self.sz   = sz

        self.lamb = lamb
        self.mu   = mu
        self.rho  = rho

        self.dx   = (xmax - xmin) / (nx - 1)
        self.dz   = (zmax - zmin) / (nz - 1)
        self.dt   = (endt - 0)    / (nt - 1)

        self.ux   = np.zeros((nz, nx))
        self.ux1  = np.zeros((nz, nx))
        self.uz   = np.zeros((nz, nx))
        self.uz1  = np.zeros((nz, nx))

        self.vx      = np.zeros((nz, nx))
        self.vx1     = np.zeros((nz, nx))
        self.vz      = np.zeros((nz, nx))
        self.vz1      = np.zeros((nz, nx))
        self.sigmaxx = np.zeros((nz, nx))
        self.sigmaxx1 = np.zeros((nz, nx))
        self.sigmazx = np.zeros((nz, nx))
        self.sigmazx1 = np.zeros((nz, nx))
        self.sigmazz = np.zeros((nz, nx))
        self.sigmazz1 = np.zeros((nz, nx))

        self.kx    = self.cal_kx()
        self.kz    = self.cal_kz()

        self.current_t  = 0
        self.current_nt = 0

        self.lamb2mu = self.lamb + self.mu * 2

        self.vpmax = np.sqrt(np.max(self.lamb2mu) / np.min(self.rho))
        self.vpmin = np.sqrt(np.min(self.lamb2mu) / np.max(self.rho)) 

        self.vsmax = np.sqrt(np.max(self.mu) / np.min(self.rho))
        self.vsmin = np.sqrt(np.min(self.mu)/ np.max(self.rho))

        self.vmax  = np.max([self.vpmax, self.vsmax])
        self.vmin  = np.min([self.vpmin, self.vsmin])
        self.dmax  = np.max([self.dx, self.dz])

        print(vars(self))

        self.stability = self.vmax * self.dt / self.dx
        print("stability: ", self.stability)
        assert(self.stability < np.sqrt(2) / np.pi)        # 稳定性条件

        self.tflimit = self.dt * self.vmax / self.dmax     # 时频采样定理
        print("tflimit:", self.tflimit)
        assert(self.tflimit < 1)

        self.splimit = self.dmax * 2 * self.fm / self.vmin # 空间采样定理
        print("splimit:", self.splimit)
        # assert(self.splimit < 1)

    def cal_kx(self):
        return np.array(
            [
                i * (np.pi / self.dx) / (self.nx / 2) if i <= self.nx / 2 else
                i * (np.pi / self.dx) / (self.nx / 2) - 2 * np.pi / self.dx
                for i in range(self.nx)
            ]
        )
    
    def cal_kz(self):
            return np.array(
            [
                i * (np.pi / self.dz) / (self.nz / 2) if i <= self.nz / 2 else
                i * (np.pi / self.dz) / (self.nz / 2) - 2 * np.pi / self.dz
                for i in range(self.nz)
            ]
        )
    
    def cal_psm_dx(self, u):
         return np.fft.ifft2(1j * self.kx * np.fft.fft2(u))

    def cal_psm_dz(self, u):
         return np.fft.ifft2(1j * self.kz * np.fft.fft2(u.T)).T

    def cal_psm_ddx(self, u):
        return np.fft.ifft2(-self.kx**2 * np.fft.fft2(u))
    
    def cal_psm_ddz(self, u):
        return np.fft.ifft2(-self.kz**2 * np.fft.fft2(u.T)).T
    
    def cal_st(self, t, dt=0.05):
        return (1 - 2 * np.pi**2 * self.fm**2 * (t-dt)**2) * np.exp(-self.fm**2 * np.pi**2 * (t-dt)**2)
    
    def cal_dt(self, v, dv):
        """caluclate t-diff value. function like:
        $$
        \frac{\partial v}{\partial t} = dv
        $$
        using one order difference method:
        $$
        \frac{\partial v}{\partial t} = \dfrac{v_{i+1} - v{i}}{dt}
        $$

        Args:
            v:  value to cal
            dv: difference value
        """
        return v + self.dt * dv

    def forward(self):
        if self.current_t >= self.endt:
            print(f"The iteration has run to the given termination time {self.endt:.3f}s, this forward() will not do nothing.")
            return

        self.ux[self.sz, self.sx] += self.cal_st(self.current_t)
        self.uz[self.sz, self.sx] += self.cal_st(self.current_t)

        coffs = np.asarray([
            1 / self.rho * (self.cal_psm_dx(self.sigmaxx) + self.cal_psm_dz(self.sigmazx)),
            1 / self.rho * (self.cal_psm_dx(self.sigmazx) + self.cal_psm_dz(self.sigmazz)),
            (self.lamb2mu) * self.cal_psm_dx(self.vx) + self.lamb * self.cal_psm_dz(self.vz),
            self.lamb * self.cal_psm_dx(self.vx) + (self.lamb2mu) * self.cal_psm_dz(self.vz),
            self.mu * (self.cal_psm_dz(self.vx) + self.cal_psm_dx(self.vz))
        ])

        res = 2 * self.dt * coffs + np.asarray([
            self.vx1, 
            self.vz1, 
            self.sigmaxx1, 
            self.sigmazz1, 
            self.sigmazx1
        ])

        TMP = np.asarray([self.vx, self.vz, self.sigmaxx, self.sigmazz, self.sigmazx]) 

        self.vx,  self.vz,  self.sigmaxx,  self.sigmazz,  self.sigmaxzx = res
        self.vx1, self.vz1, self.sigmaxx1, self.sigmazz1, self.sigmazx1 = TMP

        # self.ux += (self.dt * self.vx).real
        # self.uz += (self.dt * self.vz).real

        self.current_nt += 1
        self.current_t  += self.dt


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import time
    from utils.sfd import SFD 

    # parameters
    xmin, xmax = 0, 1024
    zmin, zmax = 0, 1024
    tmin, tmax = 0, 0.2
    dx, dz, dt = 5, 5, 5e-5
    fm = 40
    dframe = 50

    ## construct arrays
    X = np.arange(xmin, xmax, dx)
    Z = np.arange(zmin, zmax, dz)
    T = np.arange(tmin, tmax, dt)

    nx = X.shape
    nz = Z.shape
    nt = T.shape

    XX, ZZ = np.meshgrid(X, Z)

    nx, nz, nt = X.size, Z.size, T.size


    lamb = 61.3 * np.ones((nz, nx)) * 100000
    mu   = 32.2 * np.ones((nz, nx)) * 100000
    rho  = 2.7 * np.ones((nz, nx))

    # ====== simulate ========
    sim  = PSMSimulator(xmin, xmax, zmin, zmax, tmax, nx, nz, nt, fm, nx//2, nz//2, rho, lamb, mu)

    frames = nt // dframe

    UX = np.zeros((frames, nz, nx))
    UZ = np.zeros((frames, nz, nx))
    print("start simulating...")

    st = time.time()
    for frame in range(frames):
        for _ in range(dframe):
            sim.forward()
            print(f"\rprocess: {sim.current_nt}/{nt}  runtime:{time.time() - st:.2f}s", end="")
        UX[frame] = sim.vx.real
        UZ[frame] = sim.vz.real
    print("\nDone!")


    sfdx = SFD(
        xmin=xmin,
        xmax=xmax,
        ymin=zmin,
        ymax=zmax,
        endt=tmax,
        u=UX
    ) 

    sfdz = SFD(
        xmin=xmin,
        xmax=xmax,
        ymin=zmin,
        ymax=zmax,
        endt=tmax,
        u=UZ
    ) 

    sfdx.save_txt("./data/python_demo/testx.sfd")
    sfdz.save_txt("./data/python_demo/testz.sfd")


    sfd = SFD("./data/python_demo/testx.sfd")
    sfd.draw(vmin=-3e-2, vmax=5e-2, center=0)