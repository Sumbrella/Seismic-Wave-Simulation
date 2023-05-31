import matplotlib.pyplot as plt

from examples.wave_loop import wave_loop
from utils.seismic_simulator import *
from utils.boundary import Boundary
from utils.medium_config import MediumConfig
from utils.medium import Medium

def get_ricker(fm):
    def ricker(t, dt=0):
        return (1 - 2 * (np.pi * fm * (t-dt))**2) * np.exp(-(fm * np.pi* (t-dt))**2)
    return ricker
    
## parameters
xmin, xmax = 0, 1280
zmin, zmax = 0, 1280
tmin, tmax = 0, 0.2
dx, dz, dt = 5, 5, 2e-4
fm = 40


nt = int(tmax / dt)
dframe = 50
nframe = nt // dframe

nx = int((xmax - xmin) / dx)
nz = int((zmax - zmin) / dz)

C11 = 3000**2 * 2.7 * np.ones((nz, nx))
C12 = 1500**2 * 2.7 * np.ones((nz, nx))
rho = 2.7 * np.ones((nz, nx))

mcfg = MediumConfig(
    xmin,
    xmax,
    dx,
    zmin,
    zmax,
    dz,
    'I'
)

print(mcfg)


s = Source(nx//2, nz//2, lambda t: 0, get_ricker(fm))

m = Medium.get_medium(mcfg)
m.init_by_val(
    rho, C11, C12
)

b = Boundary.get_boundary("solid")
b.set_parameter(nx, nz, 0, 0)

# b = Boundary.getBoundary("atten")
# b.set_parameter(nx, nz, 60, 60, 0.0018)
    
simulator = SeismicSimulator(m, s, b, dt, tmax)

datax, dataz = wave_loop(
    simulator,
    [0.18]
)

datax.save_txt("../data/exp/3_1x.sfd")
dataz.save_txt("../data/exp/3_1z.sfd")

plt.subplot(121)
datax.plot_frame(0)

plt.subplot(122)
dataz.plot_frame(0)

plt.show()