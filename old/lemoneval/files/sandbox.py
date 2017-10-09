# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
"""Sandbox object manages multiple files in one execution of a program.

It provides a context manager for temporary directories and utilities for
multiple file types.

"""

import pathlib
import shutil
import tempfile


class TemporarySandbox(object):
    """Sandbox directory object which manages files in temporary folder.

    Attributes:
        temp_dir: `TemporaryDirectory` object, whose `name` attribute contains
            a path to temporary directory
        dir_path: `Path` object to temporary directory
        is_open: Boolean whether the temporary directory has been cleaned up

    """
    def __init__(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dir_path = pathlib.Path(self.temp_dir.name)
        self.is_open = True

    def clean_up(self):
        """Erase the temporary directory.

        This method can also be called when this object is deconstructed,
        or when the context of this object is exited.

        """
        if self.is_open:
            self.is_open = False
            self.temp_dir.cleanup()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.clean_up()

    def __del__(self):
        self.clean_up()

    def get_file_location(self, file_path):
        """Get an absolute path to a placeholder using this sandbox as root.

        Args:
            file_path: Relative path to a file placeholder.

        Returns:
            The absolute path of the given file.

        """
        file_path = pathlib.Path(file_path)
        assert(not file_path.is_absolute())
        return self.dir_path.joinpath(file_path)

    def copy_file(self, src_path, dest_path):
        """Copy the file from a given source path and return absolute path.

        Args:
            src_path: Path to the source file.
            dest_path: Relative path to the file location in this sandbox.

        Returns:
            In addition to copying the file, it returns the absolute path
            to the copied file inside this sandbox.

        """
        src_path = pathlib.Path(src_path)
        dest_path = self.get_file_location(dest_path)
        shutil.copy2(src_path, dest_path)
        return dest_path
