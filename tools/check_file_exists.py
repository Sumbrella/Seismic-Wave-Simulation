import os


def check_file_exists(filename):
    assert os.path.exists(filename), f"{filename} file doesn't find."
