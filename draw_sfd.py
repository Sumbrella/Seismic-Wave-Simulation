from utils.sfd2 import SFD
import matplotlib.pyplot as plt

datax = SFD("./data/exp/testx.sfd", ext='txt')
datay = SFD("./data/exp/testz.sfd", ext='txt')
datax.draw(seg=0.2)

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