import numpy as np 
from vedo import Grid, Text2D, show

# N = 400      # grid resolution
# A, B = 5, 4  # box sides
# end = 5      # end time
nframes = 150
nx, ny = 512, 512
xmax, ymax = 1024, 1024
end = 5
v0 = 2000
fm = 40

X, Y = np.mgrid[-xmax:xmax:nx*1j, -ymax:ymax:ny*1j]
dx, dy, dt = xmax / nx * 2, ymax / ny * 2, 0.0004

dt = 0.0004
time = np.arange(0, end, dt)

m = int(len(time)/nframes)

# initial condition (a ring-like wave)
Z0 = np.zeros_like(X)
Z1 = np.zeros_like(X)

V = np.ones_like(X) * v0

grid = Grid(s=(X[:,0], Y[0])).linewidth(0).lighting('glossy')
txt = Text2D(font='Brachium', pos='bottom-left', bg='yellow5')

cam = dict(
    position=(-118.745, -93.7215, 4454.91),
    focal_point=(-87.1933, -19.5689, -62.3707),
    viewup=(-2.91017e-3, 0.999861, 0.0163927),
    distance=4518.00,
    clipping_range=(4172.12, 4823.46),
)

plt = show(grid, txt, __doc__,
           camera=cam, axes=1, size=(1000,700), interactive=False,
)

def cal_psm_dd(U, k):
    return np.fft.ifft2(-k**2 * np.fft.fft2(U))

def cal_k(nx, dx):
    return np.array(
    [
        i * (np.pi / dx) / (nx / 2) if i <= nx / 2 else
        i * (np.pi / dx) / (nx / 2) - 2 * np.pi / dx
        for i in range(nx)
    ]
)

def source(t):
    return 10 * (1 - 2 * np.pi**2 * fm * (t-0.05)**2) * np.exp(-fm * np.pi**2 * (t-0.05)**2)

kx = cal_k(nx, dx)
ky = cal_k(ny, dy)

for i in range(nframes):
    # iterate m times before showing the frame
    for _ in range(m):
        ZC = Z1.copy()
        Z1[ny//2, nx//2] += dt**2 * source((i*m+_) * dt) # add source
        Z1 = 2 * Z1 - Z0 + \
            ((V * dt) / (dx))**2 * cal_psm_dd(Z1, kx).real + ((V * dt) / (dy))**2 * cal_psm_dd(Z1.T, ky).T.real
        Z0 = ZC

    wave = Z1.ravel()
    txt.text(f"frame: {i}/{nframes}, higth_max = {wave.max()}")
    grid.cmap("seismic", wave, vmin=-5e-5, vmax=5e-5)
    newpts = grid.points()
    newpts[:,2] = wave
    grid.points(newpts)  # update the z component
    plt.render().interactive()

plt.close()