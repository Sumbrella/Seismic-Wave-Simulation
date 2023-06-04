import os
import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anime

import constants
from tools import get_file_ext, props, plot_frame


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

    def __init__(self, file=None, ext=None, *, xmin=None, xmax=None, zmin=None, zmax=None, ts=None, u=None):
        """initialize

        Args:
            file (str, optional) .: .sfd file to be read, if None you should provide other arguments. Defaults to None.
            If the file is None, you should provide follow arguments.
            xmin (float, optional): the min value of x-axis. Defaults to None.
            xmax (float, optional): the max value of x-axis. Defaults to None.
            zmin (float, optional): the min value of z-axis. Defaults to None.
            zmax (float, optional): the max value of z-axis. Defaults to None.
            u (numpy.array, optional): 3D array, with shape(nt, nz, nx). Defaults to None.
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
            self.ts = ts
            self.data = u.copy()
            self.nt, self.nz, self.nx = self.data.shape
            self.dx = (self.xmax - self.xmin) / self.nx
            self.dz = (self.zmax - self.zmin) / self.nz

        self.vmax = np.percentile(self.data, 99) * 7.5
        self.vmin = -self.vmax

    def read_from_file(self, file, ext=None):
        """
        The read_from_file function reads in a file and stores the data into an object.

        Args:
            self: Represent the instance of the class
            file: Specify the file to read from
            ext: Specify the file extension

        Returns:
            A dictionary of the attributes
        """
        if ext is None:
            ext = constants.FORMAT_TXT
        
        if ext == constants.FORMAT_TXT:
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

        elif ext == constants.FORMAT_SFD:
            dc = np.load(file, "r")
            for key, value in dc:
                setattr(self, key, value)
        else:
            TypeError("Save Extension Not Support.")

    def plot_frame(self, index, *args, **kwargs):
        """
        The plot_frame function takes a 2D array of data and plots it as an image.
        The extent keyword argument is used to specify the x and y limits of the plot.


        Args:
            index: Select the frame to be plotted
            *args: Pass a variable number of arguments to the function
            **kwargs: Pass keyword arguments to the plot_frame function

        Returns:
            A matplotlib
        """
        kwargs.setdefault("vmin", self.vmin)
        kwargs.setdefault("vmax", self.vmax)
        return plot_frame(
            self.data[index],
            *args,
            extent=[self.xmin, self.xmax, self.zmin, self.zmax],
            **kwargs
        )

    def draw(self, figsize=constants.ONE_FIG_SHAPE, dpi=constants.FIG_DPI, seg=None, vmin=None, vmax=None,
             *args, **kwargs):
        """
        The draw function is a simple animation of the SFD file.
        It plots each frame in the SFD file, one after another, with a pause between frames.
        The user can specify how long to pause between frames (seg), as well as the size and resolution of the figure
        (figsize and dpi).

        Args:
            self: Represent the object itself
            figsize: Set the size of the figure
            dpi: Set the resolution of the image
            seg: Set the time interval between frames
            vmin: Set the minimum value of the colorbar
            vmax: Set the maximum value of the colorbar

        Returns:
            None
        """
        if vmax is None:
            vmax = self.vmax
        if vmin is None:
            vmin = self.vmin
        if seg is None:
            seg = constants.SHOW_SEG

        print("drawing sfd file...")
        plt.figure(figsize=figsize, dpi=dpi)
        for _ in range(self.nt):
            self.plot_frame(_, vmin=vmin, vmax=vmax, *args, **kwargs)
            plt.xlabel("X")
            plt.ylabel("Z")
            plt.title(f"t={self.ts[_] : .2f}s")
            plt.pause(seg)
            plt.cla()
            plt.clf()
        print("Done!")

    def save(self, fname, save_format=constants.FORMAT_TXT):
        """
        The save function saves the sfd data to a file.

        Args:
            fname: Specify the name of the file to be saved
            save_format: Determine which format of the sfd file

        Returns:
            None
        """
        if save_format == constants.FORMAT_TXT:
            self.save_txt(fname)
        elif save_format == constants.FORMAT_SFD:
            self.save_sfd(fname)
        else:
            TypeError("Save format: {} not support.".format(save_format))

    def save_sfd(self, fname):
        """
        # TODO: change binary save func
        The save_sfd function saves the data in a .sfd file.

        Args:
            self: Represent the instance of the class
            fname: Specify the file name and location to save the data

        Returns:
            None
        """
        file_ext = get_file_ext(fname)
        if file_ext != constants.FORMAT_SFD:
            fname = fname + constants.FORMAT_SFD
        print(f"saving into file {fname}")
        dc = props(self)
        np.save(fname, dc)

    def save_gif(self, fname=None, dpi=None, fps=None):
        """
        The save_gif function saves the animation as a gif file.

        Args:
            self: Represent the instance of the class
            fname: Specify the name of the file to save
            dpi: Set the resolution of the gif
            fps: Set the frame rate of the gif

        Returns:
            None
        """
        if fname is None:
            fname = "wave.gif"
        if dpi is None:
            dpi = constants.FIG_DPI
        if fps is None:
            fps = constants.GIF_FPS

        metadata = dict(title="wave field")
        writer = anime.PillowWriter(fps, metadata=metadata)
        fig = plt.figure(dpi=dpi)
        start_time = time.time()

        print(f"saving into {fname}...")
        with writer.saving(fig, fname, dpi):
            for _ in range(self.nt):
                print(f"\rprocess:{_ + 1}/{self.nt}  runtime:{time.time() - start_time:.2f}s", end="")
                self.plot_frame(_),
                plt.title("t={:.2f}s".format(self.ts[_]))
                writer.grab_frame()
                plt.cla()
                plt.clf()
        print("\nDone!")

    def save_txt(self, fname):
        """
        The save_txt function saves the data in a text file.

        Args:
            fname: Specify the file name to save the data into.

        Returns:
            None
        """
        print(f"saving into file {fname}")
        st = time.time()
        with open(fname, "w+") as fp:
            fp.write(f"{self.nx} {self.nz} {self.nt}\n")
            fp.write(f"{self.xmin} {self.xmax}\n")
            fp.write(f"{self.zmin} {self.zmax}\n")

            for i in range(self.nt):
                print(f"\r{i + 1}/{self.nt} {time.time() - st:.3f}s", end="")
                fp.write(f"{self.ts[i]}\n")
                for j in range(self.nz):
                    fp.write(" ".join([str(v) for v in self.data[i, j, :]]) + "\n")

        print("\nDone!")

    def save_png(self, save_dir, figsize=None, dpi=None):
        """
        The save_png function saves the frames of a simulation as png files.

        Args:
            self: Represent the instance of a class
            save_dir: Specify the directory where the png files will be saved
            figsize: Set the size of the figure
            dpi: Set the resolution of the image

        Returns:
            Nothing
        """
        if figsize is None:
            figsize = constants.ONE_FIG_SHAPE
        if dpi is None:
            dpi = constants.FIG_DPI

        print(f"saving pngs into dir {save_dir}")

        if not os.path.exists(save_dir):
            print(f"Path {save_dir} not exists, creating...")
            os.makedirs(save_dir)
            print(f"Create {save_dir} success.")

        start_time = time.time()
        plt.figure(figsize=figsize, dpi=dpi)
        for _ in range(self.nt):
            print(f"\rprocess:{_ + 1}/{self.nt}  runtime:{time.time() - start_time:.2f}s", end="")
            self.plot_frame(_),
            plt.title("t={:.2f}s".format(self.ts[_]))
            plt.savefig(os.path.join(save_dir, f"{_}"))
            plt.cla()
            plt.clf()

        print("\nDone!")

    def show_point(self, x, z):
        x_index = int(x / self.dx)
        z_index = int(z / self.dz)

        record = self.data[:, z_index, x_index]

        plt.plot(
            record
        )

        return record
