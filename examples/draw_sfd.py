import constants
from tools import plot_frame
from utils.sfd import SFD
import matplotlib.pyplot as plt

# datax = SFD("./data/exp/testx.sfd", ext='txt')
# datay = SFD("./data/exp/testz.sfd", ext='txt')
# datax.draw(seg=0.2)


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

# plt.figure(figsize=(9, 4), dpi=120)
# plt.subplot(121)
# datax.plot_frame(20)
# plt.subplot(122)
# datay.plot_frame(20)
# plt.show()

# plt.figure(figsize=(8.5, 4), dpi=120)
# plt.subplot(121)
# datax.plot_frame(1)
# plt.subplot(122)
# datay.plot_frame(1)
# plt.show()
