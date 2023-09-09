from examples.wave_loop import wave_loop
from utils.seismic_simulator import *
from utils.boundary import Boundary
from utils.medium_config import MediumConfig
from utils.medium import Medium


def get_ricker(fm):
    def ricker(t, dt=0):
        return (1 - 2 * (np.pi * fm * (t - dt)) ** 2) * np.exp(-(fm * np.pi * (t - dt)) ** 2)

    return ricker


## parameters
xmin, xmax = 0, 1280
zmin, zmax = 0, 1280
tmin, tmax = 0, 0.13
dx, dz, dt = 4, 4, 2e-4
fm = 40

X = np.arange(xmin, xmax, dx)
Z = np.arange(zmin, zmax, dz)
X, Z = np.meshgrid(X, Z)

nt = int(tmax / dt)
dframe = 50
nframe = nt // dframe

nx = int((xmax - xmin) / dx)
nz = int((zmax - zmin) / dz)

C11 = 4500 ** 2 * 3.8 * np.ones((nx, nz))
C12 = 4500 ** 2 / 3 * 3.8 * np.ones((nx, nz))
rho = 3.8 * np.ones((nx, nz))

C11[Z >= 600] = 3500 ** 2 * 2.8
C12[Z >= 600] = 3500 ** 2 * 2.8
rho[Z >= 600] = 2.8

C11[(Z >= 600) & (Z <= 800) & (X >= 520) & (X <= 760)] = 4500 ** 2 * 3.8
C12[(Z >= 600) & (Z <= 800) & (X >= 520) & (X <= 760)] = 4500 ** 2 * 3.8 / 3
rho[(Z >= 600) & (Z <= 800) & (X >= 520) & (X <= 760)] = 3.8

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

s = Source(nx // 2, int(500 / dx), get_ricker(fm), get_ricker(fm))

m = Medium.get_medium(mcfg)
m.init_by_val(
    rho, C11, C12
)

b = Boundary.get_boundary("solid")
b.set_parameter(nx, nz, 0, 0)

# b = Boundary.get_boundary("atten")
# b.set_parameter(nx, nz, 20, 20, 0.015)

simulator = SeismicSimulator(m, s, b, dt, tmax, use_anti_extension=True)

datax, dataz = wave_loop(
    simulator,
    use_anti_extension=True,
    is_show=True,
    show_times=20,
    is_save=True,
    save_times=50
)

datax.save_bin("data/exp/3_3x.sfd")
dataz.save_bin("data/exp/3_3z.sfd")
from examples.wave_loop import wave_loop
from utils.seismic_simulator import *
from utils.boundary import Boundary
from utils.medium_config import MediumConfig
from utils.medium import Medium


def get_ricker(fm):
    def ricker(t, dt=0):
        return (1 - 2 * (np.pi * fm * (t - dt)) ** 2) * np.exp(-(fm * np.pi * (t - dt)) ** 2)

    return ricker


## parameters
xmin, xmax = 0, 1280
zmin, zmax = 0, 1280
tmin, tmax = 0, 0.13
dx, dz, dt = 4, 4, 2e-4
fm = 40

X = np.arange(xmin, xmax, dx)
Z = np.arange(zmin, zmax, dz)
X, Z = np.meshgrid(X, Z)

nt = int(tmax / dt)
dframe = 50
nframe = nt // dframe

nx = int((xmax - xmin) / dx)
nz = int((zmax - zmin) / dz)

C11 = 4500 ** 2 * 3.8 * np.ones((nx, nz))
C12 = 4500 ** 2 / 3 * 3.8 * np.ones((nx, nz))
rho = 3.8 * np.ones((nx, nz))

C11[Z >= 600] = 3500 ** 2 * 2.8
C12[Z >= 600] = 3500 ** 2 * 2.8
rho[Z >= 600] = 2.8

C11[(Z >= 600) & (Z <= 800) & (X >= 520) & (X <= 760)] = 4500 ** 2 * 3.8
C12[(Z >= 600) & (Z <= 800) & (X >= 520) & (X <= 760)] = 4500 ** 2 * 3.8 / 3
rho[(Z >= 600) & (Z <= 800) & (X >= 520) & (X <= 760)] = 3.8

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

s = Source(nx // 2, int(500 / dx), get_ricker(fm), get_ricker(fm))

m = Medium.get_medium(mcfg)
m.init_by_val(
    rho, C11, C12
)

b = Boundary.get_boundary("solid")
b.set_parameter(nx, nz, 0, 0)

# b = Boundary.get_boundary("atten")
# b.set_parameter(nx, nz, 20, 20, 0.015)

simulator = SeismicSimulator(m, s, b, dt, tmax, use_anti_extension=True)

datax, dataz = wave_loop(
    simulator,
    use_anti_extension=True,
    is_show=True,
    show_times=20,
    is_save=True,
    save_times=50
)

datax.save_bin("data/exp/3_3x.sfd")
dataz.save_bin("data/exp/3_3z.sfd")
