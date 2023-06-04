import json

import numpy as np

from tools import check_file_exists


def cover_cmat_arg_to_matrix(cmat_arg, x, z):
    try:
        cmat_value = float(cmat_arg)
        return cmat_value * np.ones_like(z)
    except ValueError:
        ...
    try:
        cmat_arg = json.loads(cmat_arg)
        cmat_value = np.zeros_like(x)
        for value, field in cmat_arg.items():
            field = field.lower()
            cmat_value[eval(field)] = value
        return cmat_value
    except ValueError:
        ...

    check_file_exists(cmat_arg)
    cmat_value = np.loadtxt(cmat_arg)

    return cmat_value
