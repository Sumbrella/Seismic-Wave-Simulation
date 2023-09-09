import os
import time
import struct

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
    nx nz nt
    xmin xmax
    zmin zmax
    t1 t2 t3 t4 ... tn
    data(t1, x1, z1) data(t1, x2, z1) ... data(t1, xn, z1)
    ......................................................
    ......................................................
    data(t1, x1, zn) data(t1, x2, zn) ... data(t1, xn, zn)
    data(t2, x1, z1) data(t2, x2, z1) ... data(t2, xn, z1)
    ......................................................
    ......................................................
    data(t2, x1, zn) data(t2, x2, zn) ... data(t2, xn, zn)
    ......................................................
    ......................................................
    ......................................................
    ......................................................
    data(tn, x1, z1) data(tn, x2, z1) ... data(tn, xn, z1)
    ......................................................
    ......................................................
    data(tn, x1, zn) data(tn, x2, zn) ... data(tn, xn, zn)
    ------------------------------------------------------
    
    """

    def __init__(self, file=None, fmt=None, *, xmin=None, xmax=None, zmin=None, zmax=None, ts=None, u=None):
        """initialize

        Args:
            file (str, optional) : .sfd file to be read, if None you should provide other arguments. Defaults to None.
            fmt  (str, optional) : .sfd file format. choice in ['txt', 'bin'].
            If the file is None, you should provide follow arguments.
            xmin (float, optional): the min value of x-axis. Defaults to None.
            xmax (float, optional): the max value of x-axis. Defaults to None.
            zmin (float, optional): the min value of z-axis. Defaults to None.
            zmax (float, optional): the max value of z-axis. Defaults to None.
            u (numpy.array, optional): 3D array, with shape(nt, nz, nx). Defaults to None.
        """
        if fmt is None:
            fmt = 'txt'

        if fmt not in constants.SAVE_FORMATS:
            ValueError("SFD file format {} are not support. Choice in {}.".format(fmt, constants.SAVE_FORMATS))

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
            self.read_from_file(file, fmt)
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

        self.vmax = np.percentile(self.data, 99) * 7.5  # maximum value for colorbar
        self.vmin = -self.vmax                          # minimum value for colorbar

    def read_from_file(self, file, fmt=None):
        """
        The read_from_file function reads in a file and stores the data into an object.

        Args:
            self: Represent the instance of the class
            file: Specify the file to read from
            fmt: Specify the file format

        Returns:
            A dictionary of the attributes
        """
        if fmt is None:
            fmt = constants.FORMAT_TXT
        
        if fmt == constants.FORMAT_TXT:
            try:
                open(file, "r")
            except UnicodeDecodeError:
                self.read_bin(file)
            else:
                self.read_txt(file)
        elif fmt == constants.FORMAT_BIN:
            self.read_bin(file)
        else:
            TypeError("file format do not Support.")

    def read_bin(self, file):
        with open(file, "rb") as fp:
            version = ".".join([str(i) for i in np.frombuffer(fp.read(12), dtype='i')])
            print("reading file {}, version:{}".format(file, version))
            float_size = np.frombuffer(fp.read(4), dtype='i')[0]
            if float_size == 4:
                float_fmt = "f"
            elif float_size == 8:
                float_fmt = "d"
            else:
                ValueError("float size of {} can not match".format(float_size))
            self.nx, self.nz, self.nt = np.frombuffer(fp.read(12), dtype='i')
            self.xmin, self.xmax, self.zmin, self.zmax = np.frombuffer(fp.read(16), dtype='f')
            self.ts = np.frombuffer(fp.read(self.nt * float_size), dtype=float_fmt)
            self.data = np.frombuffer(fp.read(float_size * self.nx * self.nz * self.nt), dtype=float_fmt) \
                .reshape([self.nt, self.nz, self.nx])
        self.dx = (self.xmax - self.xmin) / (self.nx - 1)
        self.dz = (self.zmax - self.zmin) / (self.nz - 1)

    def read_txt(self, file):
        with open(file, "r") as fp:
            self.nx, self.nz, self.nt = [int(i) for i in fp.readline().split()]
            self.xmin, self.xmax = [float(i) for i in fp.readline().split()]
            self.zmin, self.zmax = [float(i) for i in fp.readline().split()]

            self.dx = (self.xmax - self.xmin) / (self.nx - 1)
            self.dz = (self.zmax - self.zmin) / (self.nz - 1)
            self.data = np.zeros((self.nt, self.nz, self.nx))

            self.ts = [float(i) for i in fp.readline().split()]

            for _ in range(self.nt):
                tmp = np.zeros((self.nz, self.nx))
                for i in range(self.nz):
                    tmp[i] = [float(i) for i in fp.readline().split()]
                self.data[_] = tmp.copy()

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
        start_time = time.time()
        for _ in range(self.nt):
            print(f"\rcurrent_time: {self.ts[_]:.3f},  runtime: {time.time() - start_time:.3f}s", end="")
            self.plot_frame(_, vmin=vmin, vmax=vmax, *args, **kwargs)
            plt.xlabel("X")
            plt.ylabel("Z")
            plt.title(f"t={self.ts[_] : .2f}s")
            plt.pause(seg)
            plt.cla()
            plt.clf()
        print("\nDone!")

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
        elif save_format == constants.FORMAT_BIN:
            self.save_bin(fname)
        else:
            TypeError("Save format: {} not support.".format(save_format))

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
                fp.write(str(self.ts[i]) + " ")
            fp.write("\b\n")
            for i in range(self.nt):
                for j in range(self.nz):
                    fp.write(" ".join([str(v) for v in self.data[i, j, :]]) + "\n")

        print("\nDone!")

    def save_bin(self, fname):
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
        if file_ext != ".sfd":
            fname = fname + ".sfd"
        print(f"saving into file {fname}")

        with open(fname, "wb") as fp:
            # sfd_type = np.dtype([
            #     ('version', [('0', np.int), ('1', np.int), ('2', np.int)]),
            #     ('float_size', np.int),
            #     ('nx', np.int),
            #     ('nz', np.int),
            #     ('nt', np.int),
            #     ('xmin', np.float),
            #     ('xmax', np.float),
            #     ('zmin', np.float),
            #     ('zmax', np.float),
            # ])

            for v in constants.__version__.split("."):
                fp.write(struct.pack("i", int(v)))                   # version id
            fp.write(struct.pack("i", self.data.dtype.itemsize))     # length of one float number
            fp.write(struct.pack("i", self.nx))
            fp.write(struct.pack("i", self.nz))
            fp.write(struct.pack("i", self.nt))
            fp.write(struct.pack("f", self.xmin))
            fp.write(struct.pack("f", self.xmax))
            fp.write(struct.pack("f", self.zmin))
            fp.write(struct.pack("f", self.zmax))
            fp.write(self.ts.tobytes())
            fp.write(self.data.tobytes())

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

    def show_section(
        self,
        axis,
        value,
        *args,
        **kwargs
    ):
        if type(axis) == str:
            if axis == 'x':
                axis = 1
            elif axis == 'z':
                axis = 0
            else:
                ValueError("The value of axis in function show_section should be 'x' or 'z'")

        if axis == 0:
            value = int(value / self.dz)
            section = self.data[:, value, :]
            plt.imshow(
                section,
                *args,
                aspect='auto',
                extent=[self.zmin, self.zmax, self.nt, 0],
                vmax=np.percentile(section, 99),
                vmin=-np.percentile(section, 99),
                **kwargs
            )

        elif axis == 1:
            value = int(value / self.dx)
            section = self.data[:, :, value]
            plt.imshow(
                section,
                *args,
                aspect='auto',
                extent=[self.xmin, self.xmax, self.nt, 0],
                vmax=np.percentile(section, 99) * 5,
                vmin=-np.percentile(section, 99) * 5,
                **kwargs
            )
        else:
            section = None

        plt.show()
