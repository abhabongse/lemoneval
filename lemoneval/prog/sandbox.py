# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
"""Sandbox object manages multiple files in one execution of a program.

It provides a context manager for temporary directories and utilities for
multiple file types.

"""

import os
import shutil
import tempfile


class TemporarySandbox(object):
    """Sandbox directory object which manages files in temporary folder.

    Attributes:
        temp_dir: `TemporaryDirectory` object, whose `name` attribute contains
            a path to temporary directory
        is_open: Boolean whether the temporary directory has been cleaned up

    """
    def __init__(self):
        self.temp_dir = tempfile.TemporaryDirectory()
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

    def get_empty_file_location(self, path):
        """Get an absolute path to a placeholder using this sandbox as root.

        Args:
            path: Relative path to a file placeholder.

        Returns:
            The absolute path of the given file.

        """
        assert(not os.path.isabs(path))
        return os.path.join(self.temp_dir.name, path)

    def get_file_from_src(self, src_path, dest_path):
        """Copy the file from a given source path and return absolute path.

        Args:
            src_path: Path to the source file.
            dest_path: Relative path to the file location in this sandbox.

        Returns:
            In addition to copying the file, it returns the absolute path
            to the copied file inside this sandbox.

        """
        assert(not os.path.isabs(dest_path))
        dest_path = os.path.join(self.temp_dir.name, dest_path)
        shutil.copyfile(src_path, dest_path)
        return dest_path