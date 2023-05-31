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
xmin, xmax = 0, 2560
zmin, zmax = 0, 2560
tmin, tmax = 0, 0.2
dx, dz, dt = 10, 10, 2e-4
fm = 30

X = np.arange(xmin, xmax, dx)
Z = np.arange(zmin, zmax, dz)
X, Z = np.meshgrid(X, Z)

nt = int(tmax / dt)
dframe = 50
nframe = nt // dframe

nx = int(np.ceil((xmax - xmin) / dx))
nz = int(np.ceil((zmax - zmin) / dz))

rho = 2.5 * np.ones((nz, nx))

alpha1 = 5500
alpha2 = 4500
beta1 = alpha1 / np.sqrt(3)
beta2 = alpha2 / np.sqrt(3)
epsilon1 = 0.5
gamma1 = -0.2
delta1 = 0.1
epsilon2 = 0.5
gamma2 = -0.2
delta2 = 0.1

C11 = rho * (1 + 2 * epsilon1) * alpha1 **2
C13 = rho * np.sqrt((alpha1**2 - beta1**2) * ((1 + 2 * delta1) * alpha1**2 - beta1**2)) - rho * beta1**2
C33 = rho * alpha1**2
C55 = rho * (1 + 2 * gamma1) * beta1**2

C11[X>1280] = rho[X>1280] * (1 + 2 * epsilon2) * alpha2 **2
C13[X>1280] = rho[X>1280] * np.sqrt((alpha2**2 - beta2**2) * ((1 + 2 * delta2) * alpha2**2 - beta2**2)) - rho[X>1280] * beta2**2
C33[X>1280] = rho[X>1280] * alpha2**2
C55[X>1280] = rho[X>1280] * (1 + 2 * gamma2) * beta2**2


mcfg = MediumConfig(
    xmin,
    xmax,
    dx,
    zmin,
    zmax,
    dz,
    'HTI'
)

print(mcfg)


s = Source(nx//2, nz//2, get_ricker(fm), lambda t:0)

m = Medium.getMedium(mcfg)
m.initByVal(
    rho, C11, C13, C33, C55
)

# b = Boundary.getBoundary("solid")
# b.set_parameter(nx, nz, 0, 0)

b = Boundary.getBoundary("atten")
b.set_parameter(nx, nz, 20, 20, 0.005)
    
simulator = SeismicSimulator(m, s, b, dt, tmax)

datax, dataz = wave_loop(
    simulator,
    41,
    is_show=True
)

datax.save_txt("./data/exp/4_5bx.sfd")
dataz.save_txt("./data/exp/4_5bz.sfd")

