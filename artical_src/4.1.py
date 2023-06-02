import constants
from examples.wave_loop import wave_loop
from utils.seismic_simulator import *
from utils.boundary import Boundary
from utils.medium_config import MediumConfig
from utils.medium import Medium
from utils.source import get_source_func

# parameters
xmin, xmax = 0, 1000
zmin, zmax = 0, 1000
tmin, tmax = 0, 0.2
dx, dz, dt = 3.9, 3.9, 2e-4
fm = 30

X = np.arange(xmin, xmax, dx)
Z = np.arange(zmin, zmax, dz)
X, Z = np.meshgrid(X, Z)

nt = int(tmax / dt)
dframe = 50
nframe = nt // dframe

nx = int(np.ceil((xmax - xmin) / dx))
nz = int(np.ceil((zmax - zmin) / dz))

rho = 2.17 * np.ones((nz, nx))
C11 = 26.4e6 * np.ones((nz, nx))
C13 = 6.11e6 * np.ones((nz, nx))
C33 = 15.6e6 * np.ones((nz, nx))
C44 = 4.38e6 * np.ones((nz, nx))

mcfg = MediumConfig(
    xmin,
    xmax,
    dx,
    zmin,
    zmax,
    dz,
    'VTI'
)

print(mcfg)


s = Source(nx//2, nz//2, lambda t: 0, get_source_func(constants.SOURCE_RICKER, fm))

m = Medium.get_medium(mcfg)
m.init_by_val(
    rho, C11, C13, C33, C44
)

b = Boundary.get_boundary(constants.BOUNDARY_SOLID)
b.set_parameter(nx, nz, 0, 0)

# b = Boundary.getBoundary("atten")
# b.set_parameter(nx, nz, 10, 10, 0.0005)
    
simulator = SeismicSimulator(m, s, b, dt, tmax)

datax, dataz = wave_loop(
    simulator,
    21,
    is_show=True,
    is_save=False
)

# datax.save_txt("../data/exp/4_1x.sfd")
# dataz.save_txt("../data/exp/4_1z.sfd")