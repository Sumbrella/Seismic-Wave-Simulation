import time
from typing import Union, List, Set, Tuple

import numpy as np
import matplotlib.pyplot as plt

import constants
from utils.seismic_simulator import SeismicSimulator
from tools.plot_frame import plot_frame
from utils.sfd import SFD


def wave_loop(
        s: SeismicSimulator,
        save_times: Union[List[float], int],
        is_show: bool = True,
        is_save: bool = True,
        vmin: float = None,
        vmax: float = None,
        **kwargs,
) -> Union[tuple[SFD, SFD], tuple[None, None]]:
    nt = int(s.endt / s.dt)

    # auto calculate save times, defaults to 20-step show one figure.
    if save_times is None:
        n_frame = nt // 20
        if n_frame == 0:
            n_frame = 1
        save_times = n_frame

    # change save times to type of list
    if type(save_times) == int:
        save_times = np.linspace(0, s.endt, save_times, endpoint=True)
    elif type(save_times) == list:
        save_times = np.asarray(save_times)

    print("target frame to save:", save_times)
    # cover save times into index
    save_time_index = (save_times / s.dt).astype(int)
    save_time_index = save_time_index[save_time_index < nt]

    start_time = time.time()

    if is_save:
        ux = np.zeros((len(save_time_index), s.medium.cfg.nz, s.medium.cfg.nx))
        uz = np.zeros((len(save_time_index), s.medium.cfg.nz, s.medium.cfg.nx))
    else:
        ux = None
        uz = None

    if is_show:
        plt.figure(figsize=constants.TWO_FIG_SHAPE, dpi=constants.FIG_DPI)

    j = 0
    for i in range(nt):
        s.forward()
        print("\rSimulation Process: time:{:.3f}s, runtime:{:.3f}s".format(s.current_t, time.time() - start_time),
              end="")

        if j < len(save_time_index) and i == save_time_index[j]:
            if is_save:
                ux[j] = s.ux
                uz[j] = s.uz
            j += 1

            if is_show:
                plt.subplot(121)
                if vmin is None or vmax is None:
                    plot_frame(s.ux, vmin=-np.percentile(s.ux, 99) * 7.5, vmax=np.percentile(s.ux, 99) * 7.5, **kwargs)
                else:
                    plot_frame(s.ux, vmin=vmin, vmax=vmax, **kwargs)

                plt.subplot(122)
                if vmin is None or vmax is None:
                    plot_frame(s.uz, vmin=-np.percentile(s.uz, 99) * 7.5, vmax=np.percentile(s.uz, 99) * 7.5, **kwargs)
                else:
                    plot_frame(s.uz, vmin=vmin, vmax=vmax, **kwargs)

                plt.pause(1e-3)
                plt.cla()
                plt.clf()

    print("\nSimulation Done!")

    if is_save:
        sfd_x = SFD(
            xmin=s.medium.cfg.xmin,
            xmax=s.medium.cfg.xmax,
            zmin=s.medium.cfg.zmin,
            zmax=s.medium.cfg.zmax,
            ts=save_times,
            U=ux
        )

        sfd_z = SFD(
            xmin=s.medium.cfg.xmin,
            xmax=s.medium.cfg.xmax,
            zmin=s.medium.cfg.zmin,
            zmax=s.medium.cfg.zmax,
            ts=save_times,
            U=uz
        )


        return sfd_x, sfd_z
    else:
        return None, None
