import time


import matplotlib.pyplot as plt
import matplotlib.animation as anime

import constants
from tools import plot_frame
from tools.plot_frame import plot_frame_xz
from utils.sfd import SFD


def show_xz(sfd_x: SFD, sfd_z: SFD,
            seg=None,
            figsize=None,
            dpi=None,
            vmin=None,
            vmax=None):
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

    for i, t in enumerate(sfd_x.ts):
        plot_frame_xz(sfd_x.data[i], sfd_z.data[i], fig, t, vmin=vmin, vmax=vmax)
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
            plot_frame_xz(sfd_x.data[i], sfd_z.data[i], fig, t, vmin=vmin, vmax=vmax)
            writer.grab_frame()
            plt.cla()
            plt.clf()
    print("\nDone!")
