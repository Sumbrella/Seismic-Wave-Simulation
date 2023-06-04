import argparse
import configparser

import constants


def get_parser():
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
        version='%(prog)s ' + constants.__version__,
        help='显示版本信息'
    )
    # ============================= Command Run ================================= #
    parser_run  = subparsers.add_parser(constants.COMMAND_RUN, help='run simulation')

    parser_conf = argparse.ArgumentParser(add_help=False)
    parser_conf.add_argument("--subcommand", type=str)
    parser_conf.add_argument("--conf", type=str)
    args, remaining_argv = parser_conf.parse_known_args()        

    values = {}
    if args.conf:
        config = configparser.ConfigParser()
        config.read([args.conf])
        for section in config.sections():
            values.update(dict(config.items(section)))
    
    parser_run.set_defaults(**values)
    parser_run.add_argument("--conf", type=str)

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
        '--rho'
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
        "--source_x",
        type=float
    )
    source_cfg.add_argument(
        "--source_z",
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
        choices=constants.BOUNDARY_TYPES
    )
    # # # x absorb length
    boundary_cfg.add_argument(
        "--x_absorb_length",
        type=int,
    )
    # # # z absorb length
    boundary_cfg.add_argument(
        "--z_absorb_length",
        type=int,
    )
    # # # Other arguments of absorb func
    boundary_cfg.add_argument(
        "--absorb_alpha",
        type=float
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
        "--use_anti_extension",
        action="store_true"
    )

    simulate_cfgs.add_argument(
        "--run_with_show", action="store_true"
    )

    simulate_cfgs.add_argument(
        "--show_times"
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
        default=constants.FORMAT_TXT,
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
    parser_save_png = subparsers.add_parser(constants.COMMAND_SAVE_PNG, help="save sfd file into pngs")
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

    # ======================================================================== # 

    # ======================== Show Point Command ============================ # 
    parser_show_point = subparsers.add_parser(constants.COMMAND_SHOW_POINT, help="show one point seismic record.")
    parser_show_point.add_argument(
        "--input_file",
        nargs="+"
    )
    parser_show_point.add_argument(
        "--file_format",
        type=str,
        choices=constants.SAVE_FORMATS
    )
    parser_show_point.add_argument(
        "--x",
        type=int
    )
    parser_show_point.add_argument(
        "--z",
        type=int
    )

    # ======================== Show Point Command ============================ #
    parser_show_section = subparsers.add_parser(constants.COMMAND_SHOW_SECTION, help="show one section seismic record.")
    parser_show_section.add_argument(
        "--input_file"
    )
    parser_show_section.add_argument(
        "--file_format",
        type=str,
        choices=constants.SAVE_FORMATS
    )
    parser_show_section.add_argument(
        "--axis",
        choices=["x", "z"]
    )
    parser_show_section.add_argument(
        "--value",
        type=float
    )
    parser_show_section.add_argument(
        "--cmap",
        type=str,
    )

    return parser, parser_run, parser_show, parser_save_gif, parser_save_png
