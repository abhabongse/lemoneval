# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
"""Utility functions for file handlings.
"""
import pathlib

def sanitize_file(path, absolute_only=True):
    """Make sure that file path is absolute and file does exist.

    Args:
        path: `str` or `pathlib.Path` of path to a file
        absolute_only: Boolean whether `file_path` must be specified as
            an absolute path

    Returns:
        `path` in absolute path wrapped under `pathlib.Path` ensuring that
        the file does exist
    """
    path = pathlib.Path(path)
    # Check or make the file in absolute path
    if not absolute_only:
        path = path.absolute()
    path_str = str(path)
    if absolute_only and not path.is_absolute():
        raise ValueError('file path must be absolute: {path_str!r}')
    # Check whether file exists
    if not path.exists():
        raise FileNotFoundError('file at given path not exists: {path_str!r}')
    return path
