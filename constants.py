# # Version

__version__ = "1.0.0"

# # arg commands
COMMAND_RUN      = "run"
COMMAND_DRAW_SFD = "draw"

# # medium type constants
I_MEDIUM   = "I"
VTI_MEDIUM = "VTI"
HTI_MEDIUM = "HTI"

MEDIUM_TYPES = [I_MEDIUM, VTI_MEDIUM, HTI_MEDIUM]

# # boundary type constants
SOLID_BOUNDARY = "SOLID"
ATTEN_BOUNDARY = "ATTEN"

BOUNDARY_TYPES = [SOLID_BOUNDARY, ATTEN_BOUNDARY]

# # save format
FORMAT_TXT = ".txt"
FORMAT_SFD = ".sfd"

SAVE_FORMATS = [FORMAT_SFD, FORMAT_TXT]

# # source types
SOURCE_RICKER = "ricker"

SOURCE_TYPES = [SOURCE_RICKER]

# =============== Code constants =================
ONE_FIG_SHAPE = (5, 3)
TWO_FIG_SHAPE = (9, 4)
FIG_DPI = 120
