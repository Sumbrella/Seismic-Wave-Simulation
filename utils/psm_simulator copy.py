import numpy as np 


# class PSMSimulator:
#     """simple simulator for pseudospectral method(psm) on wavefiled.
#     """
#     def __init__(
#         self,
#         xmin,
#         xmax,
#         zmin,
#         zmax,
#         endt,
#         nx,
#         nz,
#         nt,
#         fm,
#         sx,
#         sz,
#         rho,
#         C11,
#         C13,
#         C33,
#         C44
#     ):
#         """Initialize PSMSimulator

#         Args
#         --------------
#             xmin (float): the min value of x-axis
#             xmax (float): the max value of x-axis
#             zmin (float): the min value of z-axis
#             zmax (float): the max value of z-axis
#             endt (float): end time
#             nt (int): number of time
#             nx (int): number of segments of x
#             nz (int): number of segments of z
#             fm (float): main frequency of source
#             sx (int): source point of x-axis index
#             sz (int): source point of z-axis index
#             C (numpy.array): 4d array, the elastic constants, shape like (i, j, nz, nx)
#         Example
#         ---------------
#             import numpy as np
#             import matplotlib.pyplot as plt
#             import seaborn as sns
#             import time

#             ## parameters
#             xmin, xmax = -512, 512
#             zmin, zmax = -512, 512
#             tmin, tmax =  0, 2
#             dx, dz, dt = 4, 4, 0.0004
#             v0 = 2000
#             fm = 40
#             dframe = 50

#             ## construct arrays
#             X  = np.arange(xmin, xmax, dx)
#             Z  = np.arange(zmin, zmax, dz)
#             T  = np.arange(tmin, tmax, dt)

#             nx, nz, nt = X.size, Z.size, T.size

#             V  = np.ones((nz, nx)) * v0

#             from utils.psm_simulator import PSMSimulator
#             sim  = PSMSimulator(xmin, xmax, zmin, zmax, tmax, nt, nx, nz, V, fm, nx//2, nz//2)

#             frames = nt // dframe

#             U = np.zeros((frames, nz, nx))
#             print("start simulating...")

#             st = time.time()
#             for frame in range(frames):
#                 for _ in range(dframe):
#                     sim.forward()
#                 print(f"\rprocess: {sim.current_nt}/{nt}  runtime:{time.time() - st:.2f}s", end="")
#                 U[frame] = sim.u1
#             print("\nDone!")
#         """
#         self.xmin = xmin
#         self.xmax = xmax
#         self.zmin = zmin
#         self.zmax = zmax
#         self.endt = endt
#         self.nt   = nt
#         self.nx   = nx
#         self.nz   = nz
#         self.fm   = fm
#         self.sx   = sx
#         self.sz   = sz
#         self.rho  = rho

#         # self.lamb = lamb
#         # self.mu   = mu
#         self.C11  = C11
#         self.C13  = C13
#         self.C33  = C33
#         self.C44  = C44

#         self.dx   = (xmax - xmin) / (nx - 1)
#         self.dz   = (zmax - zmin) / (nz - 1)
#         self.dt   = (endt - 0)    / (nt - 1)

#         self.ux   = np.zeros((nz, nx))
#         self.uz   = np.zeros((nz, nx))
#         self.ux1  = np.zeros((nz, nx))
#         self.uz1  = np.zeros((nz, nx))

#         # self.vx      = np.zeros((nz, nx))
#         # self.vz      = np.zeros((nz, nx))
#         # self.sigmaxx = np.zeros((nz, nx))
#         # self.sigmazx = np.zeros((nz, nx))
#         # self.sigmazz = np.zeros((nz, nx))

#         self.kx    = self.cal_kx()
#         self.kz    = self.cal_kz()

#         self.current_t  = 0
#         self.current_nt = 0

#         # self.lamb2mu = self.lamb + self.mu * 2
#         # self.lambmu  = self.lamb + self.mu

#         # self.vpmax = np.sqrt(np.max(self.lamb2mu) / np.min(self.rho))
#         # self.vpmin = np.sqrt(np.min(self.lamb2mu) / np.max(self.rho)) 

#         # self.vsmax = np.sqrt(np.max(self.lambmu) / np.min(self.rho))
#         # self.vsmin = np.sqrt(np.min(self.lambmu) / np.max(self.rho))

#         # self.vmax  = np.max([self.vpmax, self.vsmax])
#         # self.vmin  = np.min([self.vpmin, self.vsmin])
#         # self.dmax  = np.max([self.dx, self.dz])

#         print(vars(self))

#         # self.stability = self.vmax * self.dt / self.dx
#         # print("stability: ", self.stability)
#         # assert(self.stability < np.sqrt(2) / np.pi)        # 稳定性条件

#         # self.tflimit = self.dt * self.vmax / self.dmax     # 时频采样定理
#         # print("tflimit:", self.tflimit)
#         # assert(self.tflimit < 1)

#         # self.splimit = self.dmax * 2 * self.fm / self.vmin # 空间采样定理
#         # print("splimit:", self.splimit)
#         # assert(self.splimit < 1)

#     def cal_kx(self):
#         return np.array(
#             [
#                 i * (np.pi / self.dx) / (self.nx / 2) if i <= self.nx / 2 else
#                 i * (np.pi / self.dx) / (self.nx / 2) - 2 * np.pi / self.dx
#                 for i in range(self.nx)
#             ]
#         )
    
#     def cal_kz(self):
#             return np.array(
#             [
#                 i * (np.pi / self.dz) / (self.nz / 2) if i <= self.nz / 2 else
#                 i * (np.pi / self.dz) / (self.nz / 2) - 2 * np.pi / self.dz
#                 for i in range(self.nz)
#             ]
#         )
    
#     def cal_psm_dx(self, u):
#          return np.fft.ifft2(1j * self.kx * np.fft.fft2(u))

#     def cal_psm_dz(self, u):
#          return np.fft.ifft2(1j * self.kz * np.fft.fft2(u.T)).T

#     def cal_psm_ddx(self, u):
#         return np.fft.ifft2(-self.kx**2 * np.fft.fft2(u))
    
#     def cal_psm_ddz(self, u):
#         return np.fft.ifft2(-self.kz**2 * np.fft.fft2(u.T)).T
    
#     def cal_st(self, t, dt=0.05):
#         return (1 - 2 * np.pi**2 * self.fm * (t-dt)**2) * np.exp(-self.fm * np.pi**2 * (t-dt)**2)

#     def cal_dt(self, v, dv):
#         """caluclate t-diff value. function like:
#         $$
#         \frac{\partial v}{\partial t} = dv
#         $$
#         using one order difference method:
#         $$
#         \frac{\partial v}{\partial t} = \dfrac{v_{i+1} - v{i}}{dt}
#         $$

#         Args:
#             v:  value to cal
#             dv: difference value
#         """
#         return v + self.dt * dv

#     def forward(self):
#         if self.current_t >= self.endt:
#             print(f"The iteration has run to the given termination time {self.endt:.3f}s, this forward() will not do nothing.")
#             return
        
#         self.ux[self.sz, self.sx] += self.dt**2 * self.cal_st(self.current_t)
#         self.uz[self.sz, self.sx] += self.dt**2 * self.cal_st(self.current_t)

#         # # # d^2 U = 
#         self.ux, self.ux1 = 2 * self.ux - self.ux1 + self.dt**2 + self.rho * (\
#             self.C11 * self.cal_psm_ddx(self.ux) +\
#             (self.C13 + self.C44) * self.cal_psm_dz(self.cal_psm_dx(self.uz)) +\
#             self.C44 * self.cal_psm_ddz(self.ux)), self.ux

#         self.uz, self.uz1 = 2 * self.uz - self.uz1 + self.dt**2 * self.rho * (\
#             self.C33  * self.cal_psm_ddz(self.uz) +\
#             (self.C13 + self.C44) * self.cal_psm_dz(self.cal_psm_dx(self.ux)) +\
#             self.C44 * self.cal_psm_ddx(self.uz)), self.uz
    

#         # self.vx[self.sz, self.sx] += self.dt**2 * self.cal_st(self.current_t)
#         # self.vz[self.sz, self.sx] += self.dt**2 * self.cal_st(self.current_t)

#         # 速度应力方程，无法运行
#         # self.ux, self.uz, self.vx, self.vz, self.sigmaxx, self.sigmazz, self.sigmazx = self.cal_dt(
#         #     np.asarray([
#         #         self.ux, self.uz, self.vx, self.vz, self.sigmaxx, self.sigmazz, self.sigmazx
#         #     ]),
#         #     np.asarray([
#         #         self.vx,
#         #         self.vz,
#         #         (self.cal_psm_dx(self.sigmaxx) + self.cal_psm_dz(self.sigmazx)) / self.rho,
#         #         (self.cal_psm_dx(self.sigmazx) + self.cal_psm_dz(self.sigmazz)) / self.rho,
#         #         (self.lamb + 2 * self.mu) * self.cal_psm_dx(self.vx) + self.lamb * self.cal_psm_dz(self.vz),
#         #         self.lamb * self.cal_psm_dx(self.vx) + (self.lamb + 2 * self.mu) * self.cal_psm_dz(self.vz),
#         #         self.mu * (self.cal_psm_dz(self.vx) + self.cal_psm_dx(self.vz))
#         #     ])
#         # )

#         self.current_nt += 1
#         self.current_t  += self.dt

# ================================================================================================================================================
## Old Version
#  Date: Apr 16 14:05


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
        Example
        ---------------
            import numpy as np
            import matplotlib.pyplot as plt
            import seaborn as sns
            import time

            ## parameters
            xmin, xmax = -512, 512
            zmin, zmax = -512, 512
            tmin, tmax =  0, 2
            dx, dz, dt = 4, 4, 0.0004
            v0 = 2000
            fm = 40
            dframe = 50

            ## construct arrays
            X  = np.arange(xmin, xmax, dx)
            Z  = np.arange(zmin, zmax, dz)
            T  = np.arange(tmin, tmax, dt)

            nx, nz, nt = X.size, Z.size, T.size

            V  = np.ones((nz, nx)) * v0

            from utils.psm_simulator import PSMSimulator
            sim  = PSMSimulator(xmin, xmax, zmin, zmax, tmax, nt, nx, nz, V, fm, nx//2, nz//2)

            frames = nt // dframe

            U = np.zeros((frames, nz, nx))
            print("start simulating...")

            st = time.time()
            for frame in range(frames):
                for _ in range(dframe):
                    sim.forward()
                print(f"\rprocess: {sim.current_nt}/{nt}  runtime:{time.time() - st:.2f}s", end="")
                U[frame] = sim.u1
            print("\nDone!")
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
        self.uz   = np.zeros((nz, nx))
        self.ux1  = np.zeros((nz, nx))
        self.uz1  = np.zeros((nz, nx))

        # self.vx      = np.zeros((nz, nx))
        # self.vz      = np.zeros((nz, nx))
        # self.sigmaxx = np.zeros((nz, nx))
        # self.sigmazx = np.zeros((nz, nx))
        # self.sigmazz = np.zeros((nz, nx))

        self.kx    = self.cal_kx()
        self.kz    = self.cal_kz()

        self.current_t  = 0
        self.current_nt = 0

        self.lamb2mu = self.lamb + self.mu * 2
        self.lambmu  = self.lamb + self.mu

        self.vpmax = np.sqrt(np.max(self.lamb2mu) / np.min(self.rho))
        self.vpmin = np.sqrt(np.min(self.lamb2mu) / np.max(self.rho)) 

        self.vsmax = np.sqrt(np.max(self.lambmu) / np.min(self.rho))
        self.vsmin = np.sqrt(np.min(self.lambmu) / np.max(self.rho))

        self.vmax  = np.max([self.vpmax, self.vsmax])
        self.vmin  = np.min([self.vpmin, self.vsmin])
        self.dmax  = np.max([self.dx, self.dz])

        print(vars(self))

        self.stability = self.vmax * self.dt / self.dx
        print("stability: ", self.stability)
        assert(self.stability < np.sqrt(2) / np.pi)                 # 稳定性条件

        self.tflimit = self.dt * self.vmax / self.dmax              # 时频采样定理
        print("tflimit:", self.tflimit)
        assert(self.tflimit < 1)

        self.splimit = self.dmax * 2 * self.fm / self.vmin          # 空间采样定理
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
    
    def cal_st(self, t):
        return (1 - 2 * np.pi**2 * self.fm * (t-0.15)**2) * np.exp(-self.fm * np.pi**2 * (t-0.15)**2)

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
        
        self.ux[self.sz, self.sx] += self.dt**2 * self.cal_st(self.current_t)
        self.uz[self.sz, self.sx] += self.dt**2 * self.cal_st(self.current_t)

        # # # d^2 U = 
        self.ux, self.ux1 = 2 * self.ux - self.ux1 + self.dt**2 * self.rho * (\
            self.lamb2mu * self.cal_psm_ddx(self.ux) +\
            self.lambmu * self.cal_psm_dz(self.cal_psm_dx(self.uz)) +\
            self.mu * self.cal_psm_ddz(self.ux)), self.ux

        self.uz, self.uz1 = 2 * self.uz - self.uz1 + self.dt**2 * self.rho * (\
            self.lamb2mu  * self.cal_psm_ddz(self.uz) +\
            self.lambmu * self.cal_psm_dz(self.cal_psm_dx(self.ux)) +\
            self.mu * self.cal_psm_ddx(self.uz)), self.uz
    

        # self.vx[self.sz, self.sx] += self.dt**2 * self.cal_st(self.current_t)
        # self.vz[self.sz, self.sx] += self.dt**2 * self.cal_st(self.current_t)

        # 速度应力方程，无法运行
        # self.ux, self.uz, self.vx, self.vz, self.sigmaxx, self.sigmazz, self.sigmazx = self.cal_dt(
        #     np.asarray([
        #         self.ux, self.uz, self.vx, self.vz, self.sigmaxx, self.sigmazz, self.sigmazx
        #     ]),
        #     np.asarray([
        #         self.vx,
        #         self.vz,
        #         (self.cal_psm_dx(self.sigmaxx) + self.cal_psm_dz(self.sigmazx)) / self.rho,
        #         (self.cal_psm_dx(self.sigmazx) + self.cal_psm_dz(self.sigmazz)) / self.rho,
        #         (self.lamb + 2 * self.mu) * self.cal_psm_dx(self.vx) + self.lamb * self.cal_psm_dz(self.vz),
        #         self.lamb * self.cal_psm_dx(self.vx) + (self.lamb + 2 * self.mu) * self.cal_psm_dz(self.vz),
        #         self.mu * (self.cal_psm_dz(self.vx) + self.cal_psm_dx(self.vz))
        #     ])
        # )

        self.current_nt += 1
        self.current_t  += self.dt
        

if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import time
    from utils.psm_simulator import PSMSimulator
    from utils.sfd import SFD 

    ## parameters
    xmin, xmax = -512, 512
    zmin, zmax = -512, 512
    tmin, tmax =  0, 1.2
    dx, dz, dt = 4, 4, 0.0004
    v0 = 2000
    fm = 40
    dframe = 50

    ## construct arrays
    X = np.arange(xmin, xmax, dx)
    Z = np.arange(zmin, zmax, dz)
    T = np.arange(tmin, tmax, dt)

    lamb = 0.01
    mu   = 0.01

    nx, nz, nt = X.size, Z.size, T.size
    
    # # ====== simulate ========
    sim  = PSMSimulator(xmin, xmax, zmin, zmax, tmax, nx, nz, nt, fm, nx//2, nz//2, 1, lamb, mu)

    frames = nt // dframe

    UX = np.zeros((frames, nz, nx))
    UZ = np.zeros((frames, nz, nx))
    print("start simulating...")

    st = time.time()
    for frame in range(frames):
        for _ in range(dframe):
            sim.forward()
        print(f"\rprocess: {sim.current_nt}/{nt}  runtime:{time.time() - st:.2f}s", end="")
        UX[frame] = sim.ux.real
        UZ[frame] = sim.uz.real
    print("\nDone!")



# ================================================================================================================================================
## Old version
## Date: Apr 14 22:28
## This version only can calculate 各项同性

# class PSMSimulator:
#     """simple simulator for pseudospectral method(psm) on wavefiled.
#     """
#     def __init__(
#         self,
#         xmin,
#         xmax,
#         ymin,
#         ymax,
#         endt,
#         nx,
#         ny,
#         nt,
#         vf,
#         fm,
#         sx,
#         sy
#     ):
#         """Initialize PSMSimulator

#         Args
#         --------------
#             xmin (float): the min value of x-axis
#             xmax (float): the max value of x-axis
#             ymin (float): the min value of y-axis
#             ymax (float): the max value of y-axis
#             endt (float): end time
#             nt (int): number of time
#             nx (int): number of segments of x
#             ny (int): number of segments of y
#             vf (numpy.array): 2d array, the speed filed, should have shape(ny, nx)
#             fm (float): main frequency of source
#             sx (int): source point of x-axis index
#             sy (int): source point of y-axis index
#         Example
#         ---------------
#             import numpy as np
#             import matplotlib.pyplot as plt
#             import seaborn as sns
#             import time

#             ## parameters
#             xmin, xmax = -512, 512
#             zmin, zmax = -512, 512
#             tmin, tmax =  0, 2
#             dx, dz, dt = 4, 4, 0.0004
#             v0 = 2000
#             fm = 40
#             dframe = 50

#             ## construct arrays
#             X  = np.arange(xmin, xmax, dx)
#             Z  = np.arange(zmin, zmax, dz)
#             T  = np.arange(tmin, tmax, dt)

#             nx, nz, nt = X.size, Z.size, T.size

#             V  = np.ones((nz, nx)) * v0

#             from utils.psm_simulator import PSMSimulator
#             sim  = PSMSimulator(xmin, xmax, zmin, zmax, tmax, nt, nx, nz, V, fm, nx//2, nz//2)

#             frames = nt // dframe

#             U = np.zeros((frames, nz, nx))
#             print("start simulating...")

#             st = time.time()
#             for frame in range(frames):
#                 for _ in range(dframe):
#                     sim.forward()
#                 print(f"\rprocess: {sim.current_nt}/{nt}  runtime:{time.time() - st:.2f}s", end="")
#                 U[frame] = sim.u1
#             print("\nDone!")
#         """
#         self.xmin = xmin
#         self.xmax = xmax
#         self.ymin = ymin
#         self.ymax = ymax
#         self.endt = endt
#         self.nt   = nt
#         self.nx   = nx
#         self.ny   = ny
#         self.vf   = vf
#         self.fm   = fm
#         self.sx   = sx
#         self.sy   = sy

#         self.dx   = (xmax - xmin) / (nx - 1)
#         self.dy   = (ymax - ymin) / (ny - 1)
#         self.dt   = (endt - 0)    / (nt - 1)

#         print(f"epsilon x: {np.max(self.vf) * self.dt / self.dx:.2f}")
#         assert(np.max(self.vf) * self.dt / self.dx <= 1 / (np.sqrt(2) * np.pi))
#         print(f"epsilon y: {np.max(self.vf) * self.dt / self.dy:.2f}")
#         assert(np.max(self.vf) * self.dt / self.dy <= 1 / (np.sqrt(2) * np.pi))

#         self.u0   = np.zeros((ny, nx))
#         self.u1   = np.zeros((ny, nx))

#         self.kx   = self.cal_kx()
#         self.ky   = self.cal_ky()

#         self.cofx = (self.vf * self.dt / self.dx)**2
#         self.cofy = (self.vf * self.dt / self.dy)**2

#         self.current_t = 0
#         self.current_nt = 0

#     def cal_kx(self):
#         return np.array(
#             [
#                 i * (np.pi / self.dx) / (self.nx / 2) if i <= self.nx / 2 else
#                 i * (np.pi / self.dx) / (self.nx / 2) - 2 * np.pi / self.dx
#                 for i in range(self.nx)
#             ]
#         )
    
#     def cal_ky(self):
#             return np.array(
#             [
#                 i * (np.pi / self.dy) / (self.ny / 2) if i <= self.ny / 2 else
#                 i * (np.pi / self.dy) / (self.ny / 2) - 2 * np.pi / self.dy
#                 for i in range(self.ny)
#             ]
#         )
    
#     def cal_psm_d(self, u, k):
#          return np.fft.ifft2(1j * k * np.fft.fft2(u))

#     def cal_psm_dd(self, u, k):
#             return np.fft.ifft2(-k**2 * np.fft.fft2(u))
    
#     def cal_st(self, t):
#         return (1 - 2 * np.pi**2 * self.fm * (t-0.15)**2) * np.exp(-self.fm * np.pi**2 * (t-0.15)**2)

#     def forward(self):
#         if self.current_t >= self.endt:
#             print(f"The iteration has run to the given termination time {self.endt:.3f}s, this forward() will not do nothing.")
#             return
#         TMP = self.u1.copy()
#         self.u1[self.sy, self.sx] += self.dt**2 * self.cal_st(self.current_t)
#         self.u1 = 2 * self.u1 - self.u0 +\
#             self.cofx * self.cal_psm_dd(self.u1, self.kx).real + \
#             self.cofy * self.cal_psm_dd(self.u1.T, self.ky).T.real 
#         self.u0 = TMP
#         self.current_nt += 1
#         self.current_t  += self.dt
