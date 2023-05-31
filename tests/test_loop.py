from examples.wave_loop import wave_loop

from utils.seismic_simulator import *
from utils.boundary import Boundary
from utils.medium_config import MediumConfig
from utils.medium import Medium

def get_ricker(fm):
    def ricker(t, dt=0.15):
        return (1 - 2 * (np.pi * fm * (t-dt))**2) * np.exp(-(fm * np.pi* (t-dt))**2)
    return ricker
    
## parameters
xmin, xmax = 0, 1024
zmin, zmax = 0, 1024
tmin, tmax = 0, 1.0
dx, dz, dt = 4, 4, 0.0005
fm = 40
nt = int(tmax / dt)
dframe = 50
nframe = nt // dframe

nx = int((xmax - xmin) / dx)
nz = int((zmax - zmin) / dz)

C11 = 50e5 * np.ones((nx, nz))
C12 = 26e5 * np.ones((nx, nz))
rho = 2.7 * np.ones((nx, nz))

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

wave_loop(
    simulator,
    "../data/tests/test_loop_ux.sfd",
    "../data/tests/test_loop_uz.sfd",
    10
)