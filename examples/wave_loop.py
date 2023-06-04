import time
from copy import deepcopy, copy
from typing import Union, List

import numpy as np
import matplotlib.pyplot as plt

import constants
from utils.seismic_simulator import SeismicSimulator
from tools.plot_frame import plot_frame_xz
from utils.sfd import SFD


def parse_save_times(nt, s, save_times):
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
    # cover save times into index
    save_time_index = (save_times / s.dt).astype(int)
    save_time_index = save_time_index[save_time_index < nt]
    return save_time_index, save_times


def wave_loop(
        s: SeismicSimulator,
        show_times: Union[List[float], int], 
        save_times: Union[List[float], int]=None,
        use_anti_extension: bool = False,
        is_show: bool = True,
        is_save: bool = True,
        seg: float = None,
        vmin: float = None,
        vmax: float = None,
        **kwargs,
):
    if not save_times:
        save_times = show_times
    if seg is None:
        seg = constants.SHOW_SEG
    if use_anti_extension:
        print("Running with anti extension.")
    nt = int(s.endt / s.dt)

    save_time_index, save_times = parse_save_times(nt, s, save_times)
    show_time_index, show_times = parse_save_times(nt, s, show_times)
    print("target frame to save:", save_times)
    print("target frame to show:", show_times)

    start_time = time.time()

    if is_save:
        ux = np.zeros((len(save_time_index), s.medium.cfg.nz, s.medium.cfg.nx))
        uz = np.zeros((len(save_time_index), s.medium.cfg.nz, s.medium.cfg.nx))
    else:
        ux = None
        uz = None
    
    if is_show:
        fig = plt.figure(figsize=constants.TWO_FIG_SHAPE, dpi=constants.FIG_DPI)
    else:
        fig = None

    save_j = 0
    show_j = 0

    for i in range(nt):
        s.forward()
        print("\rSimulation Process: time:{:.3f}s, runtime:{:.3f}s".format(s.current_t, time.time() - start_time),
              end="")

        if is_save and (save_j < len(save_time_index) and i == save_time_index[save_j]):
            ux[save_j] = s.ux if not use_anti_extension else (s.ux + s.an_ux) / 2
            uz[save_j] = s.uz if not use_anti_extension else (s.uz + s.an_uz) / 2
            save_j += 1

        if is_show and (show_j < len(show_time_index) and i == show_time_index[show_j]):

            plot_x = s.ux if not use_anti_extension else (s.ux + s.an_ux) / 2
            plot_z = s.uz if not use_anti_extension else (s.uz + s.an_uz) / 2

            plot_frame_xz(
                plot_x if not use_anti_extension else (s.ux + s.an_ux) / 2,
                plot_z if not use_anti_extension else (s.uz + s.an_uz) / 2,
                fig,
                show_times[show_j],
                vmin=vmin if vmin else -np.percentile(plot_x, 99) * 7.5,
                vmax=vmax if vmax else np.percentile(plot_x, 99) * 7.5,
                extent=[s.medium.cfg.xmin, s.medium.cfg.xmax, s.medium.cfg.zmax, s.medium.cfg.zmin],
                **kwargs
            )

            plt.pause(seg)
            plt.cla()
            plt.clf()

            show_j += 1


    print("\nSimulation Done!")

    if is_save:
        sfd_x = SFD(
            xmin=s.medium.cfg.xmin,
            xmax=s.medium.cfg.xmax,
            zmin=s.medium.cfg.zmin,
            zmax=s.medium.cfg.zmax,
            ts=save_times,
            u=ux
        )

        sfd_z = SFD(
            xmin=s.medium.cfg.xmin,
            xmax=s.medium.cfg.xmax,
            zmin=s.medium.cfg.zmin,
            zmax=s.medium.cfg.zmax,
            ts=save_times,
            u=uz
        )

        return sfd_x, sfd_z
    else:
        return None, None

