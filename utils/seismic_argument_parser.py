import argparse

import constants


class SeismicArgumentParser:
    def __init__(self):
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
            default=constants.BOUNDARY_SOLID,
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

        # =========================== Show SFD Command ============================= #
        parser_show = subparsers.add_parser(constants.COMMAND_SHOW, help="draw sfd format file")

        parser_show.add_argument(
            "--input_file",
            type=str,
            nargs="+"
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

        self.parser = parser
        self.subparsers = subparsers
        self.parser_run = parser_run
        self.parser_show = parser_show
        self.parser_save_gif = parser_save_gif
        self.parser_save_png = parser_save_png

    def parse_args(self, *args):
        return self.parser.parse_args(*args)
