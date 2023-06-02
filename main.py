#! /usr/local/python

import json
import os

import numpy as np

import constants
from examples.draw_sfd import show_xz, save_gif_xz, save_png_xz
from examples.wave_loop import wave_loop
from tools import cover_cmat_arg_to_matrix
from utils.seismic_argument_parser import SeismicArgumentParser
from utils.medium import MediumConfig, Medium
from utils.boundary import Boundary
from utils.seismic_simulator import SeismicSimulator
from utils.sfd import SFD
from utils.source import Source, get_source_func

if __name__ == "__main__":
    p = SeismicArgumentParser()
    args = p.parse_args()
    d_args = vars(args)
    print("Read Arguments:\n", json.dumps(d_args, indent=2))

    if args.subcommand == constants.COMMAND_RUN:
        # ************************** Run Command ***********************************
        # ========================== Medium Config Check ========================= #
        if any(i is None for i in [args.xmin, args.xmax, args.zmin, args.zmax]):
            p.parser_run.error("All args in 'xmin', 'xmax', 'zmin', 'zmax' are required.")

        if all(i is None for i in [args.nx, args.dx]):
            p.parser_run.error("At lease one argument in 'nx', 'dx' are required.")

        if all(i is None for i in [args.nz, args.dz]):
            p.parser_run.error("At lease one argument in 'nz', 'dz' are required.")

        if args.xmin >= args.xmax:
            p.parser_run.error("arg 'xmax' must larger than arg 'xmin'.")

        if args.zmin >= args.zmax:
            p.parser_run.error("arg 'zmax' must larger than arg 'zmin'.")

        if args.nx and not args.dx:
            args.dx = (args.xmax - args.xmin) / args.nx

        if args.nz and not args.dz:
            args.dz = (args.zmax - args.zmin) / args.nz

        if args.dx and not args.nx:
            args.nx = int(np.ceil((args.xmax - args.xmin)) / args.dx)

        if args.dz and not args.nz:
            args.nz = int(np.ceil((args.zmax - args.zmin) / args.dz))

        # Create Medium Config
        print("medium basic config:")
        medium_cfg = MediumConfig(
            xmin=args.xmin,
            xmax=args.xmax,
            dx=args.dx,
            zmin=args.zmin,
            zmax=args.zmax,
            dz=args.dz,
            medium_type=args.medium_type
        )

        # ================== Create medium ================== #
        medium = Medium.get_medium(medium_cfg)

        X = np.arange(args.xmin, args.xmax, args.dx)
        Z = np.arange(args.zmin, args.zmax, args.dz)

        X, Z = np.meshgrid(X, Z)

        if len(args.c_matrix) != len(medium.required_c):
            p.parser_run.error(f"medium type {medium.cfg.medium_type} require {len(medium.required_c)} c matrix, "
                               f"but {len(args.c_matrix)} is given.")

        # set c values
        medium_init_values = []
        rho_value = cover_cmat_arg_to_matrix(args.rho, X, Z)
        print("Read rho, Value: {}".format(rho_value))
        medium_init_values.append(rho_value)

        for cmat, cmat_attr in zip(args.c_matrix, medium.required_c):
            cmat_value = cover_cmat_arg_to_matrix(cmat, X, Z)
            print("Read {}, Value: {}".format(cmat_attr, cmat_value))
            medium_init_values.append(cmat_value)

        medium.init_by_val(*medium_init_values)

        # ================== Create Source ================ #
        if not args.sx:
            args.sx = (args.xmax - args.xmin) / 2 + args.xmin
            print("Don't read \"source_x\" argument, defaults to center of the medium: {:.2f}".format(args.sx))
        if not args.sz:
            args.sz = (args.zmax - args.zmin) / 2 + args.zmin
            print("Don't read \"source_z\" argument, defaults to center of the medium: {:.2f}".format(args.sz))

        # cover source x, source z to index
        sx = int(args.sx / args.dx)
        sz = int(args.sz / args.dz)

        # get source func
        sx_func = get_source_func(args.source_x_type, *args.source_x_args)
        sz_func = get_source_func(args.source_z_type, *args.source_z_args)

        source = Source(
            sx,
            sz,
            sx_func,
            sz_func
        )
        print(source)

        # ================== Create Boundary ================ #
        boundary = Boundary.get_boundary(args.boundary_type)
        boundary.set_parameter(
            args.nx,
            args.nz,
            args.a,
            args.b,
            *args.boundary_args
        )
        print(boundary)

        # ================= Create Simulator ================= #
        simulator = SeismicSimulator(
            medium=medium,
            source=source,
            boundary=boundary,
            endt=args.endt,
            dt=args.dt
        )

        if args.save:
            if any(i is None for i in [args.save_format, args.x_outfile, args.z_outfile, args.save_times]):
                p.parser_run.error("The argument \"save\" is True, but one of argument in "
                                   "\"save_format\", \"x_outfile\", \"z_outfile\" \"save_times\""
                                   "is not be set.")

                if type(args.save_times) not in [int, list]:
                    p.parser_run.error("The argument \"save_times\" should be int or list.")

        sfd_x, sfd_z = wave_loop(
            s=simulator,
            save_times=eval(args.save_times),
            is_save=args.save,
            is_show=args.run_with_show
        )

        if args.save:
            print("create dir: ", os.path.dirname(args.x_outfile))
            print("create dir: ", os.path.dirname(args.z_outfile))
            if not os.path.exists(os.path.dirname(args.x_outfile)):
                os.makedirs(os.path.dirname(args.x_outfile))
            if not os.path.exists(os.path.dirname(args.z_outfile)):
                os.makedirs(os.path.dirname(args.z_outfile))

            sfd_x.save(args.x_outfile, save_format=args.save_format)
            sfd_z.save(args.z_outfile, save_format=args.save_format)

    # Command show
    elif args.subcommand == constants.COMMAND_SHOW:
        files = args.input_file
        datas = [SFD(f, args.file_format) for f in files]
        if len(datas) == 1:
            datas[0].draw(
                seg=args.seg,
                dpi=args.dpi,
            )
        elif len(datas) == 2:
            show_xz(*datas, args.seg, dpi=args.dpi, vmax=args.vmax, vmin=args.vmin)  # TODO: 可以通过参数更改图片大小
        else:
            p.parser_show.error("Input file should has one or two.")

    # Command draw gif
    elif args.subcommand == constants.COMMAND_SAVE_GIF:
        files = args.input_file
        datas = [SFD(f, args.file_format) for f in files]

        if len(datas) == 1:
            datas[0].save_gif(
                args.gif_name,
                fps=args.fps,
                dpi=args.dpi
            )
        elif len(datas) == 2:
            save_gif_xz(*datas, args.gif_name, fps=args.fps, figsize=constants.TWO_FIG_SHAPE,
                        dpi=args.dpi, vmax=args.vmax, vmin=args.vmin)
        else:
            p.parser_save_gif.error("Input file should has one or two.")

    elif args.subcommand == constants.COMMAND_SAVE_PNG:
        files = args.input_file
        datas = [SFD(f, args.file_format) for f in files]

        if len(datas) == 1:
            datas[0].save_png(
                args.save_dir,
                dpi=args.dpi
            )
        elif len(datas) == 2:
            save_png_xz(*datas, args.save_dir, figsize=constants.TWO_FIG_SHAPE,
                        dpi=args.dpi, vmax=args.vmax, vmin=args.vmin)
        else:
            p.parser_save_gif.error("Input file should has one or two.")
