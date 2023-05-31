from abc import ABC, abstractclassmethod
import numpy as np

class Boundary(ABC):
    @classmethod
    def getBoundary(cls, boundaryType):
        if boundaryType == 'solid':
            return SolidBoundary()
        elif boundaryType == 'atten':
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


    @abstractclassmethod
    def apply(self, u):
        pass



class SolidBoundary(Boundary):
    def __init__(self):
        super().__init__()

    def set_parameter(self, n, m, a, b, v=0):
        super(SolidBoundary, self).set_parameter(n, m, a, b)
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


    def set_parameter(self, n, m, a, b, alpha):
        super().set_parameter(n, m, a, b)
        self.alpha = alpha
        self.GXHigh = np.exp(-(self.alpha * (self.a - self.absorbXLow[::-1]))**2)
        self.GXLow  = np.exp(-(self.alpha * (self.a - self.absorbXLow))**2)
        self.GZHigh = np.exp(-(self.alpha * (self.b - self.absorbZLow[::-1]))**2).reshape(-1, 1)
        self.GZLow  = np.exp(-(self.alpha * (self.b - self.absorbZLow))**2).reshape(-1, 1)
    
    def apply(self, u):
        u[:, self.absorbXHigh] *= self.GXHigh
        u[:, self.absorbXLow] *= self.GXLow
        u[self.absorbZHigh] *= self.GZHigh
        u[self.absorbZLow] *= self.GZLow
