#! /usr/local/python
import json
import os
import argparse

import numpy as np

import constants
import configparser
from examples.draw_sfd import show_xz, save_gif_xz, save_png_xz
from examples.wave_loop import wave_loop
from tools import cover_cmat_arg_to_matrix
from utils.medium import MediumConfig, Medium
from utils.boundary import Boundary
from utils.seismic_simulator import SeismicSimulator
from utils.sfd import SFD
from utils.source import Source, get_source_func


def main():
    parser = argparse.ArgumentParser(
        prog='seismi',
        description='',  # TODO Add description
    )
    subparsers = parser.add_subparsers(required=True, dest="subcommand")
    # version
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s' + constants.__version__,
        help='显示版本信息'
    )

    # ============================= Command Run ================================= #
    parser_run = subparsers.add_parser(constants.COMMAND_RUN, help='run simulation')
    parser_run.add_argument("--conf", type=str)
    args, remaining_argv = parser_run.parse_known_args()
    values = {}

    if args.conf:
        config = configparser.ConfigParser()
        config.read([args.conf])
        for section in config.sections():
            values.update(dict(config.items(section)))

    parser_run.set_defaults(**values)

    # # Medium Config
    medium_cfg = parser_run.add_argument_group(title="Medium Config")
    # # # Min Value of x-axis
    medium_cfg.add_argument(
        '--xmin',
        type=float,
    )
    # # # Max Value of x-axis
    medium_cfg.add_argument(
        '--xmax',
        type=float
    )
    # # # Dx
    medium_cfg.add_argument(
        '--dx',
        type=float
    )
    # # # Nx
    medium_cfg.add_argument(
        '--nx',
        type=int
    )
    # # # Min Value of z axis
    medium_cfg.add_argument(
        '--zmin',
        type=float,
    )
    # # # Max Value of z axis
    medium_cfg.add_argument(
        '--zmax',
        type=float,
    )
    # # # Dz
    medium_cfg.add_argument(
        '--dz',
        type=float
    )
    # # # Nz
    medium_cfg.add_argument(
        '--nz',
        type=int
    )
    # # # Medium Type
    medium_cfg.add_argument(
        '--medium_type',
        type=str,
        choices=constants.MEDIUM_TYPES,
    )
    # # # rho
    medium_cfg.add_argument(
        '--rho',
        default=2.7,
    )

    # # # C Argument
    medium_cfg.add_argument(
        '--c11'
    )

    medium_cfg.add_argument(
        '--c12'
    )

    medium_cfg.add_argument(
        '--c33'
    )

    medium_cfg.add_argument(
        '--c44'
    )

    medium_cfg.add_argument(
        '--c55'
    )

    # # source configs
    source_cfg = parser_run.add_argument_group(title="Source Configs")
    source_cfg.add_argument(
        "--source_x", dest="sx",
        type=float
    )
    source_cfg.add_argument(
        "--source_z", dest="sz",
        type=float
    )
    source_cfg.add_argument(
        "--source_x_type",
        type=str,
        default=constants.SOURCE_RICKER,
        choices=constants.SOURCE_TYPES
    )
    source_cfg.add_argument(
        "--source_x_args",
        nargs="*",
        default=[],
        type=float
    )
    source_cfg.add_argument(
        "--source_z_type",
        type=str,
        default=constants.SOURCE_RICKER,
        choices=constants.SOURCE_TYPES
    )

    source_cfg.add_argument(
        "--source_z_args",
        nargs="*",
        default=[],
        type=float
    )

    # # Boundary Configs
    boundary_cfg = parser_run.add_argument_group(title="Boundary Configs")

    # # # Boundary Type
    boundary_cfg.add_argument(
        "--boundary_type", dest='boundary_type',
        type=str,
        default=constants.BOUNDARY_SOLID,
        choices=constants.BOUNDARY_TYPES
    )
    # # # x absorb length
    boundary_cfg.add_argument(
        "--x_absort_length",
        type=int,
        default=0
    )
    # # # z absorb length
    boundary_cfg.add_argument(
        "--z_absort_length",
        type=int,
        default=0
    )
    # # # Other arguments of absorb func
    boundary_cfg.add_argument(
        "--boundary_args",
        type=float,
        default=[],
        nargs='*'
    )

    # # simulate Configs
    simulate_cfgs = parser_run.add_argument_group(title="Simulate Configs")
    simulate_cfgs.add_argument(
        "--simulate_time",
        type=float
    )
    simulate_cfgs.add_argument(
        "--simulate_delta_t",
        type=float
    )
    simulate_cfgs.add_argument(
        "--run_with_show", action="store_true"
    )

    # # save configs
    save_cfg = parser_run.add_argument_group(title="Save Configs")

    save_cfg.add_argument(
        "--save",
        action="store_true",
    )

    save_cfg.add_argument(
        "--save_format",
        type=str,
        default=constants.FORMAT_TXT,
        choices=constants.SAVE_FORMATS
    )

    save_cfg.add_argument(
        "--x_outfile",
        type=str,
    )

    save_cfg.add_argument(
        "--z_outfile",
        type=str
    )

    save_cfg.add_argument(
        "--show_times",
    )

    # ========================================================================== #

    # =========================== Show SFD Command ============================= #
    parser_show = subparsers.add_parser(constants.COMMAND_SHOW, help="draw sfd format file")

    parser_show.add_argument(
        "--input_file",
        type=str,
        nargs="+"
    )

    parser_show.add_argument(
        "--cmap",
        type=str,
        default="seismic"
    )

    parser_show.add_argument(
        "--file_format",
        type=str,
        choices=constants.SAVE_FORMATS
    )

    parser_show.add_argument(
        "--vmax",
        type=float
    )

    parser_show.add_argument(
        "--vmin",
        type=float
    )

    parser_show.add_argument(
        "--seg",
        type=float
    )

    parser_show.add_argument(
        "--dpi",
        type=float,
        default=constants.FIG_DPI
    )
    # ========================================================================== #

    # =========================  Save Gif Command ============================== #
    parser_save_gif = subparsers.add_parser(constants.COMMAND_SAVE_GIF, help="save sfd file to gif")

    parser_save_gif.add_argument(
        "--input_file",
        type=str,
        nargs="+"
    )

    parser_save_gif.add_argument(
        "--file_format",
        type=str,
        choices=constants.SAVE_FORMATS,
    )

    parser_save_gif.add_argument(
        "--gif_name",
        type=str
    )

    parser_save_gif.add_argument(
        "--vmax",
        type=float
    )

    parser_save_gif.add_argument(
        "--vmin",
        type=float
    )

    parser_save_gif.add_argument(
        "--fps",
        type=int
    )

    parser_save_gif.add_argument(
        "--dpi",
        type=float
    )

    # ========================================================================== #

    # =========================  Save Png Command ============================== #
    parser_save_png = subparsers.add_parser(constants.COMMAND_SAVE_PNG)

    parser_save_png.add_argument(
        "--input_file",
        type=str,
        nargs="+"
    )

    parser_save_png.add_argument(
        "--file_format",
        type=str,
        choices=constants.SAVE_FORMATS,
    )

    parser_save_png.add_argument(
        "--save_dir",
        type=str
    )

    parser_save_png.add_argument(
        "--vmax",
        type=float
    )

    parser_save_png.add_argument(
        "--vmin",
        type=float
    )

    parser_save_png.add_argument(
        "--dpi",
        type=float
    )

    args = parser.parse_args()
    d_args = vars(args)
    print("Read Arguments:\n", json.dumps(d_args, indent=2))

    if args.subcommand == constants.COMMAND_RUN:
        # ******************************** Run Command ***********************************
        # ========================== Medium Config Check ========================= #
        if any(i is None for i in [args.xmin, args.xmax, args.zmin, args.zmax]):
            parser_run.error("All args in 'xmin', 'xmax', 'zmin', 'zmax' are required.")

        if all(i is None for i in [args.nx, args.dx]):
            parser_run.error("At lease one argument in 'nx', 'dx' are required.")

        if all(i is None for i in [args.nz, args.dz]):
            parser_run.error("At lease one argument in 'nz', 'dz' are required.")

        if args.xmin >= args.xmax:
            parser_run.error("arg 'xmax' must larger than arg 'xmin'.")

        if args.zmin >= args.zmax:
            parser_run.error("arg 'zmax' must larger than arg 'zmin'.")

        if args.nx and not args.dx:
            args.dx = (args.xmax - args.xmin) / args.nx

        if args.nz and not args.dz:
            args.dz = (args.zmax - args.zmin) / args.nz

        if args.dx and not args.nx:
            args.nx = int(np.ceil((args.xmax - args.xmin)) / args.dx)

        if args.dz and not args.nz:
            args.nz = int(np.ceil((args.zmax - args.zmin) / args.dz))

        # ========================== Run Config Check ========================= #
        if not args.simulate_delta_t or not args.simulate_time:
            parser_run.error("the following arguments are required: simulate_delta_t and simulate_time")
        if not args.show_times:
            parser_run.error("the following arguments are required: --show_times")
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

        x = np.arange(args.xmin, args.xmax, args.dx)
        z = np.arange(args.zmin, args.zmax, args.dz)

        x, z = np.meshgrid(x, z)

        # set c values
        medium_init_values = []
        rho_value = cover_cmat_arg_to_matrix(args.rho, x, z)
        print("Read rho, Value: {}".format(rho_value))
        medium_init_values.append(rho_value)

        for cmat_attr in medium.required_c:
            if not getattr(args, cmat_attr):
                parser_run.error(f"the following arguments are required: --{cmat_attr}")
            cmat_value = cover_cmat_arg_to_matrix(getattr(args, cmat_attr), x, z)
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
            args.x_absort_length,
            args.z_absort_length,
            *args.boundary_args
        )
        print(boundary)

        # ================= Create Simulator ================= #
        simulator = SeismicSimulator(
            medium=medium,
            source=source,
            boundary=boundary,
            endt=args.simulate_time,
            dt=args.simulate_delta_t
        )

        if args.save:
            if any(i is None for i in [args.save_format, args.x_outfile, args.z_outfile]):
                parser_run.error("The argument \"save\" is True, but one of argument in "
                                 "\"save_format\", \"x_outfile\", \"z_outfile\" "
                                 "is not be set.")
        args.show_times = eval(args.show_times)
        if type(args.show_times) not in [int, list]:
            parser_run.error(f"The argument \"show_times\" should be int or list, but {type(args.show_times)}")

        sfd_x, sfd_z = wave_loop(
            s=simulator,
            save_times=args.show_times,
            is_save=args.save,
            is_show=args.run_with_show
        )

        if args.save:
            if not os.path.exists(os.path.dirname(args.x_outfile)):
                print("create dir: ", os.path.dirname(args.x_outfile))
                os.makedirs(os.path.dirname(args.x_outfile))
            if not os.path.exists(os.path.dirname(args.z_outfile)):
                print("create dir: ", os.path.dirname(args.z_outfile))
                os.makedirs(os.path.dirname(args.z_outfile))

            sfd_x.save(args.x_outfile, save_format=args.save_format)
            sfd_z.save(args.z_outfile, save_format=args.save_format)

    # ******************************** Command show ********************************* #
    elif args.subcommand == constants.COMMAND_SHOW:
        files = args.input_file
        datas = [SFD(f, args.file_format) for f in files]
        if len(datas) == 1:
            datas[0].draw(
                seg=args.seg,
                dpi=args.dpi,
                cmap=args.cmap,
            )
        elif len(datas) == 2:
            show_xz(*datas, args.seg, dpi=args.dpi, vmax=args.vmax, vmin=args.vmin, cmap=args.cmap)
            # TODO: 可以通过参数更改图片大小
        else:
            parser_show.error("Input file should has one or two.")

    # ****************************** Command draw gif ******************************* #
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
            parser_save_gif.error("Input file should has one or two.")

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
            parser_save_gif.error("Input file should has one or two.")


if __name__ == '__main__':
    # import sys
    # sys.argv = ['main.py', 'run', '--conf', 'configs/test.cfg']
    main()
