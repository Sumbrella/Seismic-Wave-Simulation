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
xmin, xmax = 0, 1024
zmin, zmax = 0, 1024
tmin, tmax = 0, 0.2
dx, dz, dt = 4, 4, 2e-4
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

alpha1 = 4500
alpha2 = 3600
beta1 = alpha1 / np.sqrt(3)
beta2 = alpha2 / np.sqrt(3)
epsilon = 0.3
gamma = 0.1
delta = 0.2

C11 = rho * (1 + 2 * epsilon) * alpha1 **2
C13 = rho * np.sqrt((alpha1**2 - beta1**2) * ((1 + 2 * delta) * alpha1**2 - beta1**2)) - rho * beta1**2
C33 = rho * alpha1**2
C44 = rho * beta1**2

C11[Z>500] = rho[Z>500] * (1 + 2 * epsilon) * alpha2 **2
C13[Z>500] = rho[Z>500] * np.sqrt((alpha2**2 - beta2**2) * ((1 + 2 * delta) * alpha2**2 - beta2**2)) - rho[Z>500] * beta2**2
C33[Z>500] = rho[Z>500] * alpha2**2
C44[Z>500] = rho[Z>500] * beta2**2



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


s = Source(nx//2, int(400 / dz), lambda t:0, get_ricker(fm))

m = Medium.get_medium(mcfg)
m.init_by_val(
    rho, C11, C13, C33, C44
)

# b = Boundary.getBoundary("solid")
# b.set_parameter(nx, nz, 0, 0)

b = Boundary.get_boundary("atten")
b.set_parameter(nx, nz, 15, 15, 0.002)
    
simulator = SeismicSimulator(m, s, b, dt, tmax)

datax, dataz = wave_loop(
    simulator,
    30,
    is_show=True
)

datax.save_txt("./data/exp/4_2x.sfd")
dataz.save_txt("./data/exp/4_2z.sfd")
