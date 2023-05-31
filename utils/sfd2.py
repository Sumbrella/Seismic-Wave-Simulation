import numpy as np
import matplotlib.pyplot as plt

import constants
from tools import get_file_ext, props

class SFD:
    """
    Seismic forward simulation data format.
    The txt format like this: 
    -------------------------------------------------------
    nx, nz, nt
    xmin, xmax
    zmin, zmax
    t1
    data(t1, x1, z1) data(t1, x2, z1) ... data(t1, xn, z1)
    ......................................................
    ......................................................
    data(t1, x1, zn) data(t1, x2, zn) ... data(t1, xn, zn)
    t2
    data(t2, x1, z1) data(t2, x2, z1) ... data(t2, xn, z1)
    ......................................................
    ......................................................
    data(t2, x1, zn) data(t2, x2, zn) ... data(t2, xn, zn)
    t3
    ......................................................
    ......................................................
    ......................................................
    ......................................................
    tn
    data(tn, x1, z1) data(tn, x2, z1) ... data(tn, xn, z1)
    ......................................................
    ......................................................
    data(tn, x1, zn) data(tn, x2, zn) ... data(tn, xn, zn)
    ------------------------------------------------------
    
    """

    def __init__(self, file=None, ext=None, *args, xmin=None, xmax=None, zmin=None, zmax=None, ts=None, U=None):
        """initialize

        Args:
            file (str, optional) .: .sfd file to be read, if None you should provide other arguments. Defaults to None.
            xmin (float, optional): the min value of x-axis. Defaults to None.
            xmax (float, optional): the max value of x-axis. Defaults to None.
            zmin (float, optional): the min value of z-axis. Defaults to None.
            zmax (float, optional): the max value of z-axis. Defaults to None.
            U (numpy.array, optional): 3D array, with shape(nt, nz, nx). Defaults to None.
        """
        self.xmin = None
        self.xmax = None

        self.zmin = None
        self.zmax = None

        self.dx = None
        self.dz = None 
        self.nx = None
        self.nz = None
        self.nt = None

        self.ts = None
        self.data = None

        if file is not None:
            self.read_from_file(file, ext)
        else:
            self.xmin = xmin
            self.xmax = xmax
            self.zmin = zmin
            self.zmax = zmax
            self.ts   = ts
            self.data = U.copy()
            self.nt, self.nz, self.nx = self.data.shape
            self.dx = (self.xmax - self.xmin) / (self.nx - 1)
            self.dz = (self.zmax - self.zmin) / (self.nz - 1)

        self.vmax = np.percentile(self.data, 99) * 7.5
        self.vmin = -self.vmax

    def read_from_file(self, file, ext=None):
        if ext is None:
            ext = get_file_ext(file)[1:]
        if ext == 'txt':
            with open(file, "r") as fp:
                self.nx, self.nz, self.nt = [int(i) for i in fp.readline().split()]
                self.xmin, self.xmax = [float(i) for i in fp.readline().split()]
                self.zmin, self.zmax = [float(i) for i in fp.readline().split()]

                self.dx = (self.xmax - self.xmin) / (self.nx - 1)
                self.dz = (self.zmax - self.zmin) / (self.nz - 1)
                self.data = np.zeros((self.nt, self.nz, self.nx))

                self.ts = np.ones(self.nt)

                for _ in range(self.nt):
                    ti = float(fp.readline())
                    self.ts[_] = ti
                    tmp = np.zeros((self.nz, self.nx))
                    for i in range(self.nz):
                        tmp[i] = [float(i) for i in fp.readline().split()]
                    self.data[_] = tmp.copy()

        elif ext == 'sfd':
            dc = np.load(file, "r")
            for key, value in dc:
                setattr(self, key, value)
        else:
            TypeError("Save Extension Not Support.")

    def plot_frame(self, index, *args, **kwargs):
        kwargs.setdefault('vmin', self.vmin)
        kwargs.setdefault('vmax', self.vmax)
        kwargs.setdefault('aspect', 'auto')
        kwargs.setdefault('cmap', 'seismic')
        plt.axis('equal')
        plt.imshow(
            self.data[index], 
            extent=[self.xmin, self.xmax, self.zmin, self.zmax],
            **kwargs,
        )

    def draw(self, seg=0.01, *args, vmin=None, vmax=None, center=None):
        import matplotlib.pyplot as plt

        if vmax is None:
            vmax = self.vmax
        if vmin is None:
            vmin = self.vmin

        print("drawing sfd file...")
        for _ in range(self.nt):
            self.plot_frame(_)
            plt.xlabel("X")
            plt.ylabel("Z")
            plt.title(f"t={self.ts[_] : .2f}s")
            plt.pause(seg)
            plt.cla()
            plt.clf()
        print("Done!")

    def save(self, fname, save_format=constants.FORMAT_TXT):
        if save_format == constants.FORMAT_TXT:
            self.save_txt(fname)
        elif save_format == constants.FORMAT_SFD:
            self.save_sfd(fname)
        else:
            TypeError("Save format: {} not support.".format(save_format))
    
    def save_sfd(self, fname):
        file_ext = get_file_ext(fname)
        if file_ext != '.sfd':
            fname = fname + ".sfd"
        print(f"saving into file {fname}")
        dc = props(self)
        np.save(fname, dc)
    
    def save_gif(self, fname="wave.gif", vmin=None, vmax=None, factor=1.0):
        """save the .std as gif file.

        Args:
            fname (str, optional): Filename. Defaults to "wave.gif".
            vmin (_type_, optional): The minimum value of heatmap colormap. Defaults to None.
            vmax (_type_, optional): The maximum value of heatmap colormap. Defaults to None.
            factor (float, optional): Rate of multiply speed. Defaults to 1.0.
        """
        import matplotlib.animation as anime
        import seaborn as sns
        import matplotlib.pyplot as plt
        from time import time

        fps = 1 / self.dt * factor
        if vmin is None:
            vmin = np.percentile(self.data, 99)
        if vmax is None:
            vmax = np.percentile(self.data, 1)

        metadata = dict(title="movie", artist="sumbrella")
        writer = anime.PillowWriter(fps, metadata=metadata)
        fig = plt.figure(dpi=120)
        start_time = time()

        print(f"saving into {fname}...")
        with writer.saving(fig, fname, 100):
            for _ in range(self.nt):
                print(f"\rprocess:{_ * self.dt:.2f}s/{self.endt:.2f}s  runtime:{time() - start_time:.2f}s", end="")
                sns.heatmap(self.data[_], vmin=vmin, vmax=vmax, center=0, cmap='seismic')
                plt.title(f"t={_ * self.dt : .2f}s")
                writer.grab_frame()
                plt.cla()
                plt.clf()
        print("\nDone!")


    def save_txt(self, fname):
        from time import time
        print(f"saving into file {fname}")
        st = time()
        with open(fname, "w+") as fp:
            fp.write(f"{self.nx} {self.nz} {self.nt}\n")
            fp.write(f"{self.xmin} {self.xmax}\n")
            fp.write(f"{self.zmin} {self.zmax}\n")

            for i in range(self.nt):
                print(f"\r{i + 1}/{self.nt} {time() - st:.3f}s", end="")
                fp.write(f"{self.ts[i]}\n")
                for j in range(self.nz):
                    fp.write(" ".join([str(v) for v in self.data[i, j, :]]) + "\n")

        print("\nDone!")
    
    def save_png(self, savedir, vmin=None, vmax=None, center=0, factor=1.0):
        """save the .std as a series of png file.

        Args:
            savedir (str): dir to save the png
            vmin (_type_, optional): The minimum value of heatmap colormap. Defaults to None.
            vmax (_type_, optional): The maximum value of heatmap colormap. Defaults to None.
        """
        import matplotlib.animation as anime
        import seaborn as sns
        import matplotlib.pyplot as plt
        from time import time
        import pandas as pd
        import os

        if vmin is None:
            vmin = np.min(self.data) * 0.8
        if vmax is None:
            vmax = np.max(self.data) * 0.8

        print(f"saving pngs into dir {savedir}")

        start_time = time()
        for _ in range(self.nt):
            print(f"\rprocess:{_ * self.dt:.2f}s/{self.endt:.2f}s  runtime:{time() - start_time:.2f}s", end="")
            sns.heatmap(
                data=self.data[_],
                vmin=vmin, 
                vmax=vmax, 
                center=center,
                cmap='seismic'
            )
            plt.title(f"t={_ * self.dt : .2f}s")
            plt.savefig(os.path.join(savedir, f"{_}"))
            plt.cla()
            plt.clf()
        print("\nDone!")
