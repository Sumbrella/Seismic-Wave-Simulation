import time
from typing import Union, List, Set

import numpy as np
import matplotlib.pyplot as plt

from utils.seismic_simulator import SeismicSimulator
from tools.plot_frame import plot_frame
from utils.sfd2 import SFD

def wave_loop(
    s:SeismicSimulator,
    save_times: Union[List[float], int],
    is_show:bool=True,
    vmin:float=None,
    vmax:float=None,
    **kwargs,
) -> List[SFD]:
    nt = int(s.endt / s.dt)

    # auto calculate save times, defaults to 20 step show one figure.
    if save_times is None:
        nframe = nt // 20
        if nframe == 0:
            nframe = 1
        save_times = nframe

    # change save tiems to type of list
    if type(save_times) == int:
        save_times = np.linspace(0, s.endt, save_times, endpoint=True)
    elif type(save_times) == list:
        save_times = np.asarray(save_times)

    print("target frame to save:", save_times)
    # cover save tiems into index 
    save_time_index = (save_times / s.dt).astype(int)
    save_time_index = save_time_index[save_time_index < nt]


    start_time = time.time()
    
    Ux = np.zeros((len(save_time_index), s.medium.cfg.nz, s.medium.cfg.nx))
    Uz = np.zeros((len(save_time_index), s.medium.cfg.nz, s.medium.cfg.nx))

    j = 0
    for i in range(nt):
        s.forward()
        print("\rSimulation Process: time:{:.3f}s, runtime:{:.3f}s".format(s.current_t, time.time() - start_time), end="")
        
        if j < len(save_time_index) and i == save_time_index[j]:
            Ux[j] = s.ux
            Uz[j] = s.uz
            j += 1

            if is_show:
                plt.subplot(121)
                if vmin is None or vmax is None:
                    plot_frame(s.ux, vmin=-np.percentile(s.ux, 99) * 10, vmax=np.percentile(s.ux, 99) * 10, **kwargs)
                else:
                    plot_frame(s.ux, vmin=vmin, vmax=vmax, **kwargs)

                plt.subplot(122)
                if vmin is None or vmax is None:
                    plot_frame(s.uz, vmin=-np.percentile(s.uz, 99) * 10, vmax=np.percentile(s.uz, 99) * 10, **kwargs)
                else:
                    plot_frame(s.uz, vmin=vmin, vmax=vmax, **kwargs)
                
                plt.pause(1e-3)
                plt.cla()
                plt.clf()
    print("\nSimulation Done!")

    sfdx = SFD(
        xmin=s.medium.cfg.xmin,
        xmax=s.medium.cfg.xmax,
        zmin=s.medium.cfg.zmin,
        zmax=s.medium.cfg.zmax,
        ts=save_times,
        U=Ux
    )

    # sfdx.save_txt(save_xfile_name)

    sfdz = SFD(
        xmin=s.medium.cfg.xmin,
        xmax=s.medium.cfg.xmax,
        zmin=s.medium.cfg.zmin,
        zmax=s.medium.cfg.zmax,
        ts=save_times,
        U=Uz
    )

    # sfdz.save_txt(save_zfile_name)
    return sfdx, sfdz