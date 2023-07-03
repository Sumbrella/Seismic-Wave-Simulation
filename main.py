#! /usr/local/python
import json
import os

import numpy as np

import constants
from examples.draw_sfd import show_xz, save_gif_xz, save_png_xz, show_points
from examples.wave_loop import wave_loop
from tools import cover_cmat_arg_to_matrix
from utils.seismi_parser import get_parser
from utils.medium import MediumConfig, Medium
from utils.boundary import Boundary
from utils.seismic_simulator import SeismicSimulator
from utils.sfd import SFD
from utils.source import Source, get_source_func


def main():
    parser, parser_run, parser_show, parser_save_gif, parser_save_png = get_parser()
    args = parser.parse_args()
    d_args = vars(args)
    print("Input arguments:", json.dumps(d_args, indent=2))
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
        medium_config = MediumConfig(
            xmin=args.xmin,
            xmax=args.xmax,
            dx=args.dx,
            zmin=args.zmin,
            zmax=args.zmax,
            dz=args.dz,
            medium_type=args.medium_type
        )

        # ================== Create medium ================== #
        medium = Medium.get_medium(medium_config)

        x = np.arange(args.xmin, args.xmax, args.dx)
        z = np.arange(args.zmin, args.zmax, args.dz)

        x, z = np.meshgrid(x, z)

        # set c values
        medium_init_values = []
        # get all argument name by f.__code__.co_varnames, and the first argument is self, so pass this argument.
        for cmat_attr in medium.init_by_val.__code__.co_varnames[1:]:
            if not getattr(args, cmat_attr):
                parser_run.error(f"the following arguments are required: --{cmat_attr}")
            # cover the argument cmat_attr to matrix
            cmat_value = cover_cmat_arg_to_matrix(getattr(args, cmat_attr), x, z)
            medium_init_values.append(cmat_value)

        medium.init_by_val(*medium_init_values)

        # ================== Create Source ================ #
        if not args.source_x:
            args.source_x = (args.xmax - args.xmin) / 2 + args.xmin
            print("Don't read \"source_x\" argument, defaults to center of the medium: {:.2f}".format(args.source_x))
        if not args.source_z:
            args.source_z = (args.zmax - args.zmin) / 2 + args.zmin
            print("Don't read \"source_z\" argument, defaults to center of the medium: {:.2f}".format(args.source_z))

        # cover source x, source z to index
        source_x = int(args.source_x / args.dx)
        source_z = int(args.source_z / args.dz)

        # get source func
        sx_func = get_source_func(args.source_x_type, *args.source_x_args)
        sz_func = get_source_func(args.source_z_type, *args.source_z_args)

        source = Source(
            source_x,
            source_z,
            sx_func,
            sz_func
        )
        print(source)

        # ================== Create Boundary ================ #
        if args.boundary_type is None:
            args.boundary_type = constants.BOUNDARY_SOLID
        boundary = Boundary.get_boundary(args.boundary_type)
        boundary.set_parameter(
            args.nx,
            args.nz,
            args.x_absorb_length,
            args.z_absorb_length,
            args.absorb_alpha
        )
        print(boundary)

        # ================= Create Simulator ================= #
        if type(args.use_anti_extension) == str:
            args.use_anti_extension = eval(args.use_anti_extension)
        if type(args.run_with_show) == str:
            args.run_with_show = eval(args.run_with_show)
        if type(args.save) == str:
            args.save = eval(args.save)

        simulator = SeismicSimulator(
            medium=medium,
            source=source,
            boundary=boundary,
            use_anti_extension=args.use_anti_extension,
            endt=args.simulate_time,
            dt=args.simulate_delta_t
        )

        if args.save:
            if any(i is None for i in [args.save_times, args.save_format, args.x_outfile, args.z_outfile]):
                parser_run.error("The argument \"save\" is True, but one of argument in "
                                 "\"save_format\", \"x_outfile\", \"z_outfile\" \"show_times\""
                                 "is not be set.")

            args.save_times = eval(args.save_times)
            if type(args.save_times) not in [int, list]:
                parser_run.error(f"The argument \"save_times\" should be int or list, but {type(args.show_times)}")
                
        if args.run_with_show:
            args.show_times = eval(args.show_times)
            if type(args.show_times) not in [int, list]:
                parser_run.error(f"The argument \"show_times\" should be int or list, but {type(args.show_times)}")

        d_args = vars(args)
        print("Parsed Arguments:\n", json.dumps(d_args, indent=2))

        sfd_x, sfd_z = wave_loop(
            s=simulator,
            use_anti_extension=args.use_anti_extension,
            show_times=args.show_times,
            save_times=args.save_times,
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
            parser_show.error("Input file should be one or two.")

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
            parser_save_gif.error("Input file should be one or two.")

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
            parser_save_png.error("Input file should has one or two.")
    
    elif args.subcommand == constants.COMMAND_SHOW_POINT:
        files = args.input_file
        datas = [SFD(f, args.file_format) for f in files]
        show_points(datas, args.x, args.z)

    elif args.subcommand == constants.COMMAND_SHOW_SECTION:
        # TODO: 增加arg检查
        file = args.input_file
        data = SFD(file, args.file_format)
        data.show_section(args.axis, args.value, cmap=args.cmap)


if __name__ == '__main__':
    import sys
    # sys.argv = ["main.py", "run", "--conf", "configs/test.cfg"]
    main()
