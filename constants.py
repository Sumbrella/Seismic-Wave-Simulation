# # Version

__version__ = "1.0.0"

# # arg commands
COMMAND_RUN  = "run"
COMMAND_SHOW = "show"
COMMAND_SAVE_GIF = "save_gif"
COMMAND_SAVE_PNG = "save_png"

# # medium type constants
I_MEDIUM   = "I"
VTI_MEDIUM = "VTI"
HTI_MEDIUM = "HTI"

MEDIUM_TYPES = [I_MEDIUM, VTI_MEDIUM, HTI_MEDIUM]

# # boundary type constants
BOUNDARY_SOLID = "SOLID"
BOUNDARY_ATTEN = "ATTEN"

BOUNDARY_TYPES = [BOUNDARY_SOLID, BOUNDARY_ATTEN]

# # save format
FORMAT_TXT = ".txt"
FORMAT_SFD = ".sfd"

SAVE_FORMATS = [FORMAT_SFD, FORMAT_TXT]

# # source types
SOURCE_NONE = "none"
SOURCE_RICKER = "ricker"

SOURCE_TYPES = [SOURCE_NONE, SOURCE_RICKER]

# =============== Code constants =================
ONE_FIG_SHAPE = (4, 3)
TWO_FIG_SHAPE = (9, 4)
FIG_DPI = 120
GIF_FPS = 10
SHOW_SEG = 0.1
