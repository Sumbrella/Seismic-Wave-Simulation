import numpy as np
import matplotlib.pyplot as plt


def cal_psm_k(n, k):
    res = np.array(
            [i if i <= n // 2 else i - n for i in range(n)]
        ) * k
    return res


def psm(f):
    from numpy.fft import ifft, fft
    n = f.shape[0]
    return np.real(ifft(
        fft(f) * 1j * cal_psm_k(n, dx)
    ))


def psm2(f):
    from numpy.fft import fft, ifft
    kx2 = cal_psm_k(n*2, kx[1])
    f2 = np.concatenate([f, -f])
    return np.real(ifft(fft(f2) * 1j * kx2))[:n]


fm = 10
n = 512
x = np.linspace(0, 1, n)
dx = x[1] - x[0]
x2 = np.concatenate([x, x+x[-1]])
print(dx)
# x = np.cos(2 * np.pi * 5 * t) # + np.cos(2 * np.pi * 10 * t)
f = np.sin(2 * np.pi * fm * x)
df = -2 * np.pi * fm * np.sin(2 * np.pi * fm * x)

dk = np.pi * 2 / n / dx

kx = cal_psm_k(n, dk)
kx2 = cal_psm_k(n*2, kx[1])

# plt.subplot(211)
# plt.scatter(x, kx)
# plt.subplot(212)
# plt.scatter(x2, kx2)
# plt.show()
#
# plt.figure()
# plt.subplot(131)
# plt.plot(df)
#
# plt.subplot(132)
# plt.plot(psm(f))
#
# plt.subplot(133)
# plt.plot(psm2(f))
#
# plt.show()

fft_f1 = np.fft.fft(f)
fft_f2 = np.fft.fft(np.concatenate([f, -f]))
plt.subplot(211)
plt.plot(fft_f1)
plt.subplot(212)
plt.plot(fft_f2)
plt.show()
