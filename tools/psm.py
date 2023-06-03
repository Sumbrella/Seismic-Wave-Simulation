from numpy.fft import fft2, ifft2
import numpy as np


def cal_psm_k(n, k):
    res = np.array(
            [i if i <= n / 2 else i - n for i in range(n)]
        ) * k
    return res


def cal_dx(u, kx):
    return np.real(np.fft.ifft2(1j * kx * np.fft.fft2(u)))


def cal_ddx(u, kx):
    return np.real(np.fft.ifft2(-kx ** 2 * np.fft.fft2(u)))


def cal_dz(u, kz):
    return np.real(np.fft.ifft2(1j * kz * np.fft.fft2(u.T))).T


def cal_ddz(u, kz):
    return np.real(np.fft.ifft2(-kz ** 2 * np.fft.fft2(u.T))).T
