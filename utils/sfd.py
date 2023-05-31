import os
import numpy as np

from tools import getFileExt, props

class SFD:
    """
    Seismic forward simulation data format
    -----------
    nx, nz, nt
    xmin, xmax
    zmin, zmax
    endt
    i
    data(1, 1) data(1, 2) ...
    ...
    i + 1
    ...
    ...
    nt
    data(1, 1) data(1, 2) ...
    ...
    ----------
    """

    def __init__(self, file=None, *args, xmin=None, xmax=None, zmin=None, zmax=None, endt=None, U=None):
        """initialize

        Args:
            file (str, optional): .sfd file to read, if None you should provide other arguments. Defaults to None.
            xmin (float, optional): the min value of x-axis. Defaults to None.
            xmax (float, optional): the max value of x-axis. Defaults to None.
            zmin (float, optional): the min value of y-axis. Defaults to None.
            zmax (float, optional): the max value of y-axis. Defaults to None.
            endt (float, optional): end time. Defaults to None.
            U (numpy.array, optional): 3D array, with shape(nt, nz, nx). Defaults to None.

        Example:
        # from .sfd file
        data = SFD(file="./data/python_demo/test.sfd")
        # ----------------------------
        # from data
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

            from utils.sfd import SFD
            sfd = SFD(
                xmin=xmin,
                xmax=xmax,
                zmin=zmin,
                zmax=zmax,
                endt=tmax,
                U=U
            )
            sfd.save_txt("./data/python_demo/test.sfd")
            sfd.save_gif()
        """
        self.xmin = None
        self.xmax = None

        self.zmin = None
        self.zmax = None

        self.endt = None

        self.dx = None
        self.dz = None 
        self.dt = None
        self.nx = None
        self.nz = None
        self.nt = None

        self.data = None

        if file is not None:
            self.read_from_file(file)
        else:
            self.xmin = xmin
            self.xmax = xmax
            self.zmin = zmin
            self.zmax = zmax
            self.endt = endt
            self.data = U.copy()
            self.nt, self.nz, self.nx = self.data.shape
            self.dx = (self.xmax - self.xmin) / (self.nx - 1)
            self.dz = (self.zmax - self.zmin) / (self.nz - 1)
            self.dt = (self.endt - 0) / (self.nt - 1) 

        # self.x = np.linspace(self.xmin, self.xmax, self.nx)
        # self.z = np.linspace(self.zmin, self.zmax, self.nz)

    def read_from_file(self, file, ext=None):
        from tools import get_file_ext

        if not ext:
            file_ext = get_file_ext(file)
        else:
            file_ext = ext
        
        if file_ext == '.txt':
            with open(file, "r") as fp:
                self.nx, self.nz, self.nt = [int(i) for i in fp.readline().split()]
                self.xmin, self.xmax = [float(i) for i in fp.readline().split()]
                self.zmin, self.zmax = [float(i) for i in fp.readline().split()]
                self.endt = float(fp.readline())

                self.dx = (self.xmax - self.xmin) / (self.nx - 1)
                self.dz = (self.zmax - self.zmin) / (self.nz - 1)
                self.dt = (self.endt - 0) / (self.nt - 1)
                self.data = np.zeros((self.nt, self.nz, self.nx))

                for _ in range(self.nt):
                    idx = int(fp.readline())
                    tmp = np.zeros((self.nz, self.nx))
                    for i in range(self.nz):
                        tmp[i] = [float(i) for i in fp.readline().split()]
                    self.data[_] = tmp.copy()
        elif file_ext == 'sfd':
            dc = np.load(file, "r")
            self.nx, self.nz, self.nt = dc['nx'], dc['nz'], dc['nt']
            self.xmin, self.xmax = dc['xmin'], dc['xmax']
            self.zmin, self.zmax = dc['zmin'], dc['zmax']
            self.endt = dc['endt']

            self.dx = (self.xmax - self.xmin) / (self.nx - 1)
            self.dz = (self.zmax - self.zmin) / (self.nz - 1)
            self.dt = (self.endt - 0) / (self.nt - 1)

            self.data = dc['data']
        else:
            TypeError("File Extension not support.")
        
    
    def draw(self, *args, vmin=None, vmax=None, center=None):
        import matplotlib.pyplot as plt
        import seaborn as sns

        if vmax is None:
            vmax = np.percentile(self.data, 95) * 1e3
        if vmin is None:
            vmin = -vmax

        print("drawing sfd file...")
        for _ in range(self.nt):
            print(f"\r{_ * self.dt:.2f}s/{self.endt:.2f}s", end="")
            sns.heatmap(self.data[_], vmin=vmin, vmax=vmax, center=center, cmap='seismic')
            plt.title(f"t={_ * self.dt : .2f}s")
            plt.pause(self.dt / 2)
            plt.cla()
            plt.clf()
        print("\nDone!")
    
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

    def save_sfd(self, fname):
        file_ext = getFileExt(fname)
        if file_ext != '.sfd':
            fname = fname + ".sfd"
        print(f"saving into file {fname}")
        dc = props()
        np.save(fname, dc)


    def save_txt(self, fname):
        from time import time
        print(f"saving into file {fname}")
        st = time()
        with open(fname, "w+") as fp:
            fp.write(f"{self.nx} {self.nz} {self.nt}\n")
            fp.write(f"{self.xmin} {self.xmax}\n")
            fp.write(f"{self.zmin} {self.zmax}\n")
            fp.write(f"{self.endt}\n")

            for i in range(self.nt):
                print(f"\r{i + 1}/{self.nt} {time() - st:.3f}s", end="")
                fp.write(f"{i}\n")
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
