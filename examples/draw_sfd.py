import constants
from tools import plot_frame
from utils.sfd import SFD
import matplotlib.pyplot as plt


def draw_xz(sfd_x: SFD, sfd_z: SFD, seg=0.01, figsize=constants.TWO_FIG_SHAPE, dpi=constants.FIG_DPI):
    plt.figure(figsize=figsize, dpi=dpi)
    for i, t in enumerate(sfd_x.ts):
        plt.subplot(2, 1, 1)
        plot_frame(sfd_x.data[i])
        plt.subplot(2, 1, 2)
        plot_frame(sfd_z.data[i])
        plt.pause(seg)
        plt.cla()
        plt.clf()
