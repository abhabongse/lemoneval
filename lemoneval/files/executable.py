# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
"""A Python wrapper over an executable file.
"""
import os
import pathlib
import shutil
import subprocess
import time
from .sandbox import TemporarySandbox
from .util import sanitize_file


class Executable(object):
    """Provides a callable wrap over external executable script.

    Attributes:
        exec_path: Path to executable file

    """
    def __init__(self, exec_path):
        exec_path = sanitize_file(exec_path)
        if not (os.access(exec_path, os.X_OK)):
            exec_path_str = str(exec_path)
            raise PermissionError(f"file {exec_path_str!r} not executable")
        self.exec_path = exec_path

    def __call__(self, input_fname, output_fname, time_limit=60):
        """Run the executable with given input, and print to given output.

        The function will block up to the time limit.

        Args:
            input_fname: Path to input file carrying contents to be redirected
                to standard input
            output_fname: Path to output file to which the standard output
                is redirected
            time_limit: Seconds before timeout (default: 60 seconds)

        """
        with TemporarySandbox() as sandbox:
            local_input_fname = sandbox.copy_file(input_fname, 'input.txt')
            local_output_fname = sandbox.get_file_location('output.txt')

            with open(local_input_fname) as fin, \
                 open(local_output_fname, 'w') as fout:

                start_time = time.time()
                try:
                    subprocess.run(
                        [self.exec_path], stdin=fin, stdout=fout,
                        stderr=subprocess.DEVNULL, timeout=time_limit,
                        check=True
                        )
                except subprocess.TimeoutExpired as e:
                    raise
                except subprocess.CalledProcessError as e:
                    raise
                duration = time.time() - start_time

            # Copy the file back to the specified location.
            shutil.copy2(local_output_fname, output_fname)

            # TODO: write report file into sandbox directory
