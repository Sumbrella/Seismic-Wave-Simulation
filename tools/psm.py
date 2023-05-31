from numpy.fft import fft2, ifft2
import numpy as np

def cal_psm(x, kx, order, axis):
    if axis not in [0, 1]:
        ValueError("Psm function parameter 'axis' should be 0 or 1, 0->x, 1->z")
    if axis == 0:
        return np.real(ifft2((1j * kx)**order * fft2(x.T)).T)
    else:
        return np.real(ifft2((1j * kx)**order * fft2(x)))
    

def cal_psm_dx(u, kx):
    return np.real(np.fft.ifft2(1j * kx * np.fft.fft2(u)))

def cal_psm_dz(u, kz):
    return np.real(np.fft.ifft2(1j * kz * np.fft.fft2(u.T))).T

def cal_psm_ddx(u, kx):
    return np.real(np.fft.ifft2(-kx**2 * np.fft.fft2(u)))

def cal_psm_ddz(u, kz):
    return np.real(np.fft.ifft2(-kz**2 * np.fft.fft2(u.T))).T