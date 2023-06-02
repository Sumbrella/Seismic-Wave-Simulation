import constants
import numpy as np


def get_none(*args):
    def none(t):
        return 0

    return none


def get_ricker(fm, dt=0.0, *args):
    def ricker(t):
        return (1 - 2 * (np.pi * fm * (t - dt)) ** 2) * np.exp(-(fm * np.pi * (t - dt)) ** 2)

    return ricker


def get_source_func(source_type, *source_args):
    return source_dict[source_type](*source_args)


source_dict = {
    constants.SOURCE_NONE: get_none,
    constants.SOURCE_RICKER: get_ricker
}


class Source:
    def __init__(self, sx, sz, source_fx, source_fz):
        self.sx = sx
        self.sz = sz
        self.sfx = source_fx
        self.sfz = source_fz

    def get_x_response(self, t):
        return self.sfx(t)

    def get_z_response(self, t):
        return self.sfz(t)

    def __str__(self):
        return f"""\
--------------------------- Source Config --------------------------------
source_x_index: {self.sx} \t source_z_index: {self.sz}
--------------------------------------------------------------------------
"""
