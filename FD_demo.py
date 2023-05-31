import os

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class WaveEquation2D:
    # initify horizion wave equation 2d simulator.
    def __init__(self, mt, mx, my, nt, nx, ny, px, py, v, sep):
        self.mt = mt
        self.mx = mx
        self.my = my
        self.nt = nt
        self.nx = nx
        self.ny = ny
        self.v = np.array(v)
        self.sep = sep

        self.dx = self.mx / self.nx
        self.dy = self.my / self.ny
        self.dt = self.mt / self.nt

        self.x = np.arange(0, self.mx + self.dx, self.dx)
        self.y = np.arange(0, self.my + self.dy, self.dy)
        self.t = np.arange(0, self.mt + self.dt, self.dt)

        self.u0 = lambda r, c: 0.2 * \
            np.exp(-((r - px)**2 + (c - py)**2) / 0.01)
        self.v0 = lambda r, c: 0

        r = 4 * max(self.v) ** 2 * self.dt ** 2 / (self.dx ** 2 + self.dy ** 2)
        assert r < 1, f"r should be less then 1, r is {r}."

        self.Ax = self.v * self.dt / self.dx
        self.Ay = self.v * self.dt / self.dy
        self.rx = self.Ax ** 2
        self.ry = self.Ay ** 2
        self.rxy = 1 - self.rx - self.ry

        self.u = np.zeros((self.nt + 1, self.nx + 1, self.ny + 1))

        for i in range(1, self.nx):
            for j in range(1, self.ny):
                self.u[0, i, j] = self.u0(self.x[i], self.y[j])

        self.mask = np.array(
                [[sep(self.x[i], self.y[j]) for j in range(0, ny + 1)]
                 for i in range(0, nx + 1)]
             )

    def info(self):
        print("wave arguments:")
        print(f"dx: {self.dx}, dy: {self.dy}, dt:{self.dt}")
        print(f"ax: {self.Ax}, ay: {self.Ay}")
        print(f"rx: {self.rx}, ry: {self.ry}, rxy: {self.rxy}")

    def apply_boundary(self, t):
        # absort 1 dim
        for i in range(self.nx + 1):
            self.u[t, i, 0] =\
                self.Ay[self.mask[i, 1]] * self.u[t-1, i, 1] + \
                (1 - self.Ay[self.mask[i, 0]]) * self.u[t-1, i, 0]

            self.u[t, i, self.ny] =\
                self.Ay[self.mask[i, self.ny - 1]] * \
                self.u[t-1, i, self.ny-1] + \
                (1-self.Ay[self.mask[i, self.ny]]) * self.u[t-1, i, self.ny]

        for j in range(self.ny + 1):
            self.u[t, 0, j] =\
                self.Ax[self.mask[1, j]] * self.u[t-1, 1, j] + \
                (1 - self.Ax[self.mask[0, j]]) * self.u[t-1, 0, j]

            self.u[t, self.nx, j] =\
                self.Ax[self.mask[self.nx-1, j]] * \
                self.u[t-1, self.nx-1, j] + \
                (1-self.Ax[self.mask[self.nx, j]]) * self.u[t-1, self.nx, j]

    def solve(self):
        # solve t == 1
        for i in range(1, self.nx):
            for j in range(1, self.ny):
                self.u[1, i, j] =\
                    0.5 * self.rx[self.mask[i-1, j]] * self.u[0, i-1, j] + \
                    0.5 * self.rx[self.mask[i+1, j]] * self.u[0, i+1, j] + \
                    0.5 * self.ry[self.mask[i, j-1]] * self.u[0, i, j-1] + \
                    0.5 * self.ry[self.mask[i, j+1]] * self.u[0, i, j+1] + \
                    self.rxy[self.mask[i, j]] * self.u[0, i, j] + \
                    self.dt * self.v0(i, j)
        for t in range(2, self.nt):
            print('\rsolving step {} / {}'.format(t + 1, self.nt), end="")
            # fills boundary conditios
            self.apply_boundary(t)
            for i in range(1, self.nx):
                for j in range(1, self.ny):
                    self.u[t, i, j] = \
                        self.rx[self.mask[i-1, j]] * self.u[t-1, i-1, j] + \
                        self.rx[self.mask[i+1, j]] * self.u[t-1, i+1, j] + \
                        self.ry[self.mask[i, j-1]] * self.u[t-1, i, j-1] + \
                        self.ry[self.mask[i, j+1]] * self.u[t-1, i, j+1] + \
                        2 * self.rxy[self.mask[i, j]] * self.u[t-1, i, j] -\
                        self.u[t-2, i, j]

    def plot(self, img_path="./image", show=True, save=True):
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        for t in range(0, self.nt):
            sns.heatmap(
                self.u[t, :, :],
                vmin=-np.max(self.u)/10,
                vmax=np.max(self.u)/10,
                cmap='seismic',
                xticklabels=False,
                yticklabels=False
            )
            if save:
                plt.savefig(os.path.join(img_path, str(t)))
            if show:
                plt.pause(0.01)
            plt.cla()
            plt.clf()


if __name__ == '__main__':
    we = WaveEquation2D(
        mt=1.5,
        mx=4,
        my=4,
        nt=600,
        nx=160,
        ny=160,
        px=2,
        py=2,
        v=[3.0, 5.0],
        sep=lambda r, c: 1 if r > 3 and c < 1 else 0
    )

    we.solve()
    we.plot(show=True, save=True)

