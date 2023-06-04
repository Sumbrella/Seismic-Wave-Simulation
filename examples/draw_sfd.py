import time
import os
from typing import List

import matplotlib.pyplot as plt
import matplotlib.animation as anime

import constants
from tools.plot_frame import plot_frame_xz
from utils.sfd import SFD


def show_xz(
        sfd_x: SFD,
        sfd_z: SFD,
        seg=None,
        figsize=None,
        dpi=None,
        vmin=None,
        vmax=None,
        *args, **kwargs
):
    if seg is None:
        seg = constants.SHOW_SEG
    if figsize is None:
        figsize = constants.TWO_FIG_SHAPE
    if dpi is None:
        dpi = constants.FIG_DPI
    if vmin is None:
        vmin = sfd_x.vmin
    if vmax is None:
        vmax = sfd_x.vmax

    fig = plt.figure(figsize=figsize, dpi=dpi)
    start_time = time.time()
    for i, t in enumerate(sfd_x.ts):
        print(f"\rprocess:{i + 1}/{sfd_x.nt}  runtime:{time.time() - start_time:.2f}s", end="")
        plot_frame_xz(
            sfd_x.data[i], sfd_z.data[i], 
            fig, t, 
            vmin=vmin, vmax=vmax, 
            extent=[sfd_x.xmin, sfd_x.xmax, sfd_x.zmax, sfd_x.zmin],
            *args, **kwargs
        )
        plt.pause(seg)
        plt.cla()
        plt.clf()


def save_gif_xz(sfd_x: SFD, sfd_z: SFD, fname=None, fps=None, figsize=None, dpi=None, vmin=None, vmax=None):
    if fname is None:
        fname = "wave.gif"
    if fps is None:
        fps = constants.GIF_FPS
    if figsize is None:
        figsize = constants.TWO_FIG_SHAPE
    if dpi is None:
        dpi = constants.FIG_DPI
    if vmin is None:
        vmin = sfd_x.vmin
    if vmax is None:
        vmax = sfd_x.vmax

    metadata = dict(title="wave field")
    writer = anime.PillowWriter(fps, metadata=metadata)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    start_time = time.time()
    print(f"saving into {fname}...")
    with writer.saving(fig, fname, dpi):
        for i, t in enumerate(sfd_x.ts):
            print(f"\rprocess:{i + 1}/{sfd_x.nt}  runtime:{time.time() - start_time:.2f}s", end="")
            plot_frame_xz(sfd_x.data[i], sfd_z.data[i], fig, t, vmin=vmin, vmax=vmax,
                          extent=[sfd_x.xmin, sfd_x.xmax, sfd_x.zmax, sfd_x.zmin])
            writer.grab_frame()
            plt.cla()
            plt.clf()
    print("\nDone!")


def save_png_xz(sfd_x: SFD, sfd_z: SFD, save_dir=None, figsize=None, dpi=None, vmin=None, vmax=None):
    if figsize is None:
        figsize = constants.ONE_FIG_SHAPE
    if dpi is None:
        dpi = constants.FIG_DPI
    if vmin is None:
        vmin = sfd_x.vmin
    if vmax is None:
        vmax = sfd_x.vmax

    print(f"saving pngs into dir {save_dir}")

    if not os.path.exists(save_dir):
        print(f"Path {save_dir} not exists, creating...")
        os.makedirs(save_dir)
        print(f"Create {save_dir} success.")

    start_time = time.time()
    fig = plt.figure(figsize=figsize, dpi=dpi)
    for i, t in enumerate(sfd_x.ts):
        print(f"\rprocess:{i + 1}/{sfd_x.nt}  runtime:{time.time() - start_time:.2f}s", end="")
        plot_frame_xz(sfd_x.data[i], sfd_z.data[i], fig, t, vmin=vmin, vmax=vmax,
                      extent=[sfd_x.xmin, sfd_x.xmax, sfd_x.zmax, sfd_z.zmim]
        )
        plt.savefig(os.path.join(save_dir, f"{i}"))
        plt.cla()
        plt.clf()


def show_points(datas: List[SFD], x, z):
    n = len(datas)
    for i, data in enumerate(datas):
        plt.subplot(n, 1, i + 1)
        data.show_point(x, z)
    plt.show()
