import os
import numpy as np
from .medium import Medium
from .source import Source
from .boundary import Boundary


class SeismicSimulator:
    """
    initialized by simulation base parameter

    """

    def __init__(
            self,
            medium: Medium,
            source: Source,
            boundary: Boundary,
            dt: float = 0.1,
            endt: float = 1,
            equationType: str = 'Wave',  # wave or velocity
            timeDomainMethod: str = 'FD2',  # TODO: ADD METHODS
            spaceDomainMethod: str = 'PSM',  # TODO: ADD METHODS
    ):

        self.medium = medium
        self.boundary = boundary
        self.source = source

        self.timeDomainMethod = timeDomainMethod
        self.spaceDoaminMethod = spaceDomainMethod

        self.dt = dt
        self.endt = endt
        self.ux = np.zeros(shape=medium.cfg.shape)
        self.uz = np.zeros(shape=medium.cfg.shape)

        if timeDomainMethod == 'FD2':
            self.lux = self.ux.copy()
            self.luz = self.uz.copy()

        self.current_nt = 0
        self.current_t = 0

        self.check_stability()

    def check_stability(self):
        vpmax = self.medium.vpmax
        dx = self.medium.cfg.dx
        dz = self.medium.cfg.dz

        print("Simulation Stability: {:.4f}".format(vpmax * self.dt / np.min([dx, dz])))
        print("Wave Spread from top to bottom need time {:.4f}s".format(
            (self.medium.cfg.xmax - self.medium.cfg.xmin) / vpmax))

        assert (vpmax * self.dt / np.min([dx, dz])) < (np.sqrt(2) / np.pi), \
            "Stability Can't pass, the value of (vmax * dt / dx) is {:.3f}, which should less than {:.3f}" \
                .format(vpmax * self.dt / np.min([dx, dz]), np.sqrt(2) / np.pi)

    def forward(self):
        if self.check_end():
            print("Process Completed!")
            return

        self.ux[self.source.sz, self.source.sx] += self.dt ** 2 / self.medium.rho[
            self.source.sz, self.source.sx] * self.source.get_x_response(self.current_t)
        self.uz[self.source.sz, self.source.sx] += self.dt ** 2 / self.medium.rho[
            self.source.sz, self.source.sx] * self.source.get_z_response(self.current_t)

        self.time_step()

        self.boundary.apply(self.ux)
        self.boundary.apply(self.uz)

        self._update_t()

    def time_step(self):
        if self.timeDomainMethod == 'FD2':
            cux, cuz = [self.ux, self.uz]
            self.ux, self.uz = 2 * np.asarray([self.ux, self.uz]) - np.asarray([self.lux, self.luz]) + \
                               self.dt ** 2 / self.medium.rho * self.medium.calculate_step_value(self.ux, self.uz)
            self.lux, self.luz = [cux, cuz]

    def check_end(self):
        if self.current_t >= self.endt:
            return True
        return False

    def _update_t(self):
        self.current_nt += 1
        self.current_t += self.dt
