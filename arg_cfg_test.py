import argparse
import json
import os

import numpy as np

import constants
from examples.wave_loop import wave_loop
from tools import check_file_exists, cover_cmat_arg_to_matrix

from utils.medium import MediumConfig, Medium
from utils.boundary import Boundary
from utils.seismic_simulator import SeismicSimulator
from utils.source import Source, get_source_func
from utils.sfd2 import SFD

parser = argparse.ArgumentParser(
    prog='seismi',
    description='',  # TODO Add description
)
subparsers = parser.add_subparsers(required=True, dest="subcommand")

# version
parser.add_argument('-v', '--version', action='version', version='%(prog)s' + constants.__version__,
                    help='显示版本信息')

# ============================= Command Run ================================= #
parser_run = subparsers.add_parser(constants.COMMAND_RUN, help='run simulation')
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
    required=True
)

# # # rho
medium_cfg.add_argument(
    '--rho',
    default=2.7,
)

# # # C Argument
medium_cfg.add_argument(
    '--c_matrix',
    nargs='*'
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
    default=constants.SOLID_BOUNDARY,
    choices=constants.BOUNDARY_TYPES
)
# # # X absorb length
boundary_cfg.add_argument(
    "--x_absort_length", dest='a',
    type=int,
    default=0
)
# # # Z absorb length
boundary_cfg.add_argument(
    "--z_absort_length", dest='b',
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
    "--simulate_time", dest="endt",
    type=float,
    required=True
)
simulate_cfgs.add_argument(
    "--simulate_delta_t", dest="dt",
    type=float,
    required=True
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
    "--save_times",
)

# ========================================================================== #

argv = [
    'run',
    '--xmin',
    '0',
    '--xmax',
    '1024',
    '--nx',
    '256',
    '--zmin',
    '0',
    '--zmax',
    '1024',
    '--nz',
    '256',
    '--medium_type',
    'I',
    '--c_matrix',
    '{"24300000": "...", "28500000": "(X>=100) & (X <= 900)"}',
    '6075000',
    "--source_x_args",
    "40",
    "--source_z_args",
    "40",
    "--simulate_time",
    "0.2",
    "--simulate_delta_t",
    "2e-4",
    "--save_times",
    "10",
    "--run_with_show"
]

args = parser.parse_args(argv)
d_args = vars(args)
print("Read Arguments:\n", json.dumps(d_args, indent=2))

if args.subcommand == constants.COMMAND_RUN:
    # ************************** Run Command ***********************************
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
        parser_run.error(f"medium type {medium.cfg.medium_type} require {len(medium.required_c)} c matrix, "
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
        if any(i is None for i in [args.save_format, args.x_out_file, args.z_out_file, args.save_times]):
            parser_run.error("The argument \"save\" is True, but one of argument in "
                             "\"save_format\", \"x_out_file\", \"z_out_file\" \"save_times\""
                             "is not be set.")

            if type(args.save_times) not in [int, list]:
                parser_run.error("The argument \"save_times\" should be int or list.")

    sfd_x, sfd_z = wave_loop(
        s=simulator,
        save_times=eval(args.save_times),
        is_save=args.save,
        is_show=args.run_with_show
    )

    if args.save:
        print("create dir: ", os.path.dirname(args.x_out_file))
        print("create dir: ", os.path.dirname(args.z_out_file))
        os.makedirs(os.path.dirname(args.x_out_file))
        os.makedirs(os.path.dirname(args.z_out_file))

        sfd_x.save(args.out_file_x, save_format=args.save_format)
        sfd_z.save(args.out_file_z, save_format=args.save_format)

    print("Done!")
