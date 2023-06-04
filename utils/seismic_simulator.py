import numpy as np
from .medium import Medium
from .source import Source
from .boundary import Boundary


def time_fd2(field_now, field_last, dt, time_factor):
    tmp = field_now
    field_now = 2 * field_now - field_last + dt**2 * time_factor
    field_last = tmp
    return field_now, field_last


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
            space_domain_method: str = 'PSM',  # TODO: ADD METHODS
            use_anti_extension: bool = False
    ):
        self.medium = medium
        self.boundary = boundary
        self.source = source

        self.space_domain_method = space_domain_method
        self.use_anti_extension = use_anti_extension

        self.dt = dt
        self.endt = endt

        self.ux = np.zeros(shape=medium.cfg.shape)
        self.uz = np.zeros(shape=medium.cfg.shape)

        self.lux = np.zeros(shape=medium.cfg.shape)
        self.luz = np.zeros(shape=medium.cfg.shape)

        if self.use_anti_extension:
            self.an_ux = np.zeros(shape=medium.cfg.shape)
            self.an_uz = np.zeros(shape=medium.cfg.shape)

            self.an_lux = np.zeros(shape=medium.cfg.shape)
            self.an_luz = np.zeros(shape=medium.cfg.shape)

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

    def apply_source(self):
        self.ux[self.source.sz, self.source.sx] += self.dt ** 2 / self.medium.rho[
            self.source.sz, self.source.sx] * self.source.get_x_response(self.current_t)
        self.uz[self.source.sz, self.source.sx] += self.dt ** 2 / self.medium.rho[
            self.source.sz, self.source.sx] * self.source.get_z_response(self.current_t)

        if self.use_anti_extension:
            self.an_ux[self.source.sz, self.source.sx] += self.dt ** 2 / self.medium.rho[
                self.source.sz, self.source.sx] * self.source.get_x_response(self.current_t)
            self.an_uz[self.source.sz, self.source.sx] += self.dt ** 2 / self.medium.rho[
                self.source.sz, self.source.sx] * self.source.get_z_response(self.current_t)

    def forward(self):
        if self.check_end():
            print("Process Completed!")
            return

        self.apply_source()
        self.time_step()

        # apply boundary
        self.boundary.apply(self.ux)
        self.boundary.apply(self.uz)

        if self.use_anti_extension:
            self.boundary.apply(self.an_ux)
            self.boundary.apply(self.an_uz)

        self._update_t()

    def time_step(self):
        (self.ux, self.uz), (self.lux, self.luz) = time_fd2(
            np.asarray([self.ux, self.uz]),
            np.asarray([self.lux, self.luz]),
            self.dt,
            1 / self.medium.rho * self.medium.calculate_step_value(self.ux, self.uz)
        )

        if self.use_anti_extension:
            (self.an_ux, self.an_uz), (self.an_lux, self.an_luz) = time_fd2(
                np.asarray([self.an_ux, self.an_uz]),
                np.asarray([self.an_lux, self.an_luz]),
                self.dt,
                1 / self.medium.rho * self.medium.calculate_step_value(self.an_ux, self.an_uz, self.use_anti_extension)
            )

    def check_end(self):
        if self.current_t >= self.endt:
            return True
        return False

    def _update_t(self):
        self.current_nt += 1
        self.current_t += self.dt
