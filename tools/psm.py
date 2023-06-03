from numpy.fft import fft2, ifft2
import numpy as np


def cal_psm_k(n, k):
    res = np.array(
            [i if i <= n / 2 else i - n for i in range(n)]
        ) * k
    return res


def cal_dx(u, kx):
    return np.real(np.fft.ifft2(1j * kx * np.fft.fft2(u)))

    # else:
    #     n = len(kx)
    #     kx2 = cal_psm_k(n*2, kx[1] / 2)
    #     u2_anti = np.concatenate([u, -u], axis=1)
    #     u_anti = np.real(np.fft.ifft2(1j * kx2 * np.fft.fft2(u2_anti)))[:, :n]
    #     return u_anti


def cal_ddx(u, kx):
    return np.real(np.fft.ifft2(-kx ** 2 * np.fft.fft2(u)))
    # else:
    #     n = len(kx)
    #     kx2 = cal_psm_k(n*2, kx[1] / 2)
    #     u2_anti = np.concatenate([u, -u], axis=1)
    #     u_anti = np.real(np.fft.ifft2(-kx2**2 * np.fft.fft2(u2_anti)))[:, :n]
    #     return u_anti


def cal_dz(u, kz):
    return np.real(np.fft.ifft2(1j * kz * np.fft.fft2(u.T))).T
    # else:
    #     n = len(kz)
    #     kz2 = cal_psm_k(n*2, kz[1] / 2)
    #     u2_anti = np.concatenate([u.T, -u.T], axis=1)
    #     u_anti = np.real(np.fft.ifft2(1j * kz2 * np.fft.fft2(u2_anti)))[:, :n].T
    #     return u_anti


def cal_ddz(u, kz):
    return np.real(np.fft.ifft2(-kz ** 2 * np.fft.fft2(u.T))).T
    # n = len(kz)
    # kz2 = cal_psm_k(n*2, kz[1] / 2)
    # u2_anti = np.concatenate([u.T, -u.T], axis=1)
    # u_anti = np.real(np.fft.ifft2(-kz2**2 * np.fft.fft2(u2_anti)))[:, :n].T
    # return u_anti
