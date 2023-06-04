import numpy as np


def cal_psm_k(n, k):
    res = np.array(
            [i if i <= n / 2 else i - n for i in range(n)]
        ) * k
    return res


def cal_dx(u, kx2):
    u2 = np.concatenate([u, -u], axis=1)
    u_anti = np.real(np.fft.ifft2(1j * kx2 * np.fft.fft2(u2)))[:, :u.shape[1]]
    return u_anti


def cal_ddx(u, kx2):
    u2 = np.concatenate([u, -u], axis=1)
    u_anti = np.real(np.fft.ifft2(-kx2**2 * np.fft.fft2(u2)))[:, :u.shape[1]]
    return u_anti


def cal_dz(u, kz2):
    u2 = np.concatenate([u.T, -u.T], axis=1)
    u_anti = np.real(np.fft.ifft2(1j * kz2 * np.fft.fft2(u2)))[:, :u.shape[0]].T
    return u_anti


def cal_ddz(u, kz2):
    u2 = np.concatenate([u.T, -u.T], axis=1)
    u_anti = np.real(np.fft.ifft2(-kz2**2 * np.fft.fft2(u2)))[:, :u.shape[0]].T
    return u_anti
