from abc import ABC, abstractmethod

import numpy as np

import constants


class Boundary(ABC):
    @classmethod
    def get_boundary(cls, boundary_type):
        if boundary_type == constants.BOUNDARY_SOLID:
            return SolidBoundary()
        elif boundary_type == constants.BOUNDARY_ATTEN:
            return AttenBoundary()

    def __init__(self):
        self.n = None
        self.m = None 
        self.a = None
        self.b = None

        self.absorbXHigh = None
        self.absorbXLow  = None
        self.absorbZHigh = None
        self.absorbZLow  = None

        self.boundary_type = None
    
    # 这里不能使用抽象方法，子类无法通过该函数修改父类变量
    def set_parameter(self, n, m, a, b):
        self.n = n
        self.m = m
        self.a = a
        self.b = b

        self.absorbXHigh = np.arange(n-a, n)
        self.absorbXLow  = np.arange(0, a)
        self.absorbZHigh = np.arange(n-b, n)
        self.absorbZLow  = np.arange(0, b)

    @abstractmethod
    def apply(self, u):
        pass

    def __str__(self):
        return f"""\
-------------------------- Boundary Config -------------------------------
Absorb Length X: {self.a} \t Absorb Length Z: {self.b}
Absorb Boundary Type: {self.boundary_type}
--------------------------------------------------------------------------
"""


class SolidBoundary(Boundary):
    def __init__(self):
        super().__init__()
        self.v = None
        self.boundary_type = constants.BOUNDARY_SOLID

    def set_parameter(self, n, m, a, b, v=None):
        super(SolidBoundary, self).set_parameter(n, m, a, b)
        if v is None:
            v = 0
        self.v = v
    
    def apply(self, u):
        u[self.absorbXHigh] = self.v
        u[self.absorbXLow]  = self.v

        u[:, self.absorbZHigh] = self.v
        u[:, self.absorbZLow]  = self.v


class AttenBoundary(Boundary):
    def __init__(self):
        super().__init__()
        self.alpha = None
        self.GXHigh = None
        self.GXLow = None
        self.GZHigh = None
        self.GZLow = None

        self.boundary_type = constants.BOUNDARY_ATTEN

    def set_parameter(self, n, m, a, b, alpha=None):
        super().set_parameter(n, m, a, b)
        if alpha is None:
            alpha = 0.01
        print("atten absort alpha value: {:.2f}".format(alpha))
        self.alpha = alpha

        self.GXHigh = np.exp(-(self.alpha * (self.a - self.absorbXLow[::-1])**2))
        self.GXLow  = np.exp(-(self.alpha * (self.a - self.absorbXLow)**2))
        self.GZHigh = np.exp(-(self.alpha * (self.b - self.absorbZLow[::-1])**2)).reshape(-1, 1)
        self.GZLow  = np.exp(-(self.alpha * (self.b - self.absorbZLow)**2)).reshape(-1, 1)
    
    def apply(self, u):
        u[:, self.absorbXHigh] *= self.GXHigh
        u[:, self.absorbXLow] *= self.GXLow
        u[self.absorbZHigh] *= self.GZHigh
        u[self.absorbZLow] *= self.GZLow
