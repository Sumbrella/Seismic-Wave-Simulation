import argparse, configparser

import constants

parser = argparse.ArgumentParser(
    prog='seismi',
    description='', # TODO Add description
)
subparsers = parser.add_subparsers(required=True, dest="subcommand")

## version  # TODO: 增加版本信息
parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0', help='显示版本信息')

# ============================= Command Run ================================= #
parser_run = subparsers.add_parser('run', help='run simulation')
## Medium Config
medium_cfg = parser_run.add_argument_group(title="Medium Config")

### Min Value of x axis
medium_cfg.add_argument(
    '--xmin',
    default=0,
    type=float,
)

### Max Value of x axis
medium_cfg.add_argument(
    '--xmax',
    type=float
)

### Dx
medium_cfg.add_argument(
    '--dx',
    type=float
)

### Nx
medium_cfg.add_argument(
    '--nx',
    type=int
)

### Min Value of z axis
medium_cfg.add_argument(
    '--zmin', 
    default=0,
    type=float,
)
### Max Value of z axis
medium_cfg.add_argument(
    '--zmax', 
    type=float,
)
### Dz
medium_cfg.add_argument(
    '--dz',
    type=float
)

### Nz
medium_cfg.add_argument(
    '--nz',
    type=int
)

### Medium Type
medium_cfg.add_argument(
    '--medium_type', 
    type=str,
    choices=constants.MEDIUM_TYPES
)


## Boundary Configs
boundary_cfg = parser_run.add_argument_group(title="Boundary Configs")

### Boundary Type
boundary_cfg.add_argument(
    "--boundary_type", metavar='boundaryType',
    type=str,
    choices=constants.BOUNDARY_TYPES
)
### X absorb length
boundary_cfg.add_argument(
    "--x_absort_length", metavar='a',
    type=int,
    default=0
)
### Z absorb length
boundary_cfg.add_argument(
    "--z_absort_length", metavar='b',
    type=int,
    default=0
)
### Other parameters
boundary_cfg.add_argument(
    "--other_args",
    type=float,
    default=[0.01],
    nargs='*'
)



## ========================================================================== #

argv = [
    'run',
    '--xmax',
    '1024',
    '--zmax',
    '1024',
    '--other_args',
    '1',
    '2'
]

args = parser.parse_args(argv)
print(args)



# ========================== Medium Config Check  ======================== #