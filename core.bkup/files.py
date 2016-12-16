# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
import os.path
import shutil
import subprocess


class BaseFile(object):
    """
    Base File class for use in sandbox directory.
    """
    def __init__(self, path):
        self.path = os.path.abspath(path)

    def open(self, *args, **kwargs):
        """
        Open the file with the open() built-in function routine.
        """
        return open(self.path, *args, **kwargs)

    def exists(self):
        """
        Checks if the file already exists (and is not a symlink).
        """
        return os.path.isfile(self.path)

    @property
    def basename(self):
        """
        Returns the file name without the directory.
        """
        return os.path.basename(self.path)

    @property
    def dirname(self):
        """
        Returns the directory containing the file.
        """
        return os.path.dirname(self.path)

    def copy_to(self, dest):
        """
        Make a copy of the file at the given destination.
        """
        dest = os.path.abspath(dest)
        shutil.copyfile(self.path, dest)
        return BaseFile(dest)

    def move_to(self, dest):
        """
        Move the file to the given destination.
        """
        dest = os.path.abspath(dest)
        shutil.move(self.path, dest)
        self.path = dest


class TextFile(BaseFile):
    """
    Text file class for use in sandbox directory.
    """
    pass


class SourceFile(TextFile):
    """
    Source file class for use in sandbox directory.
    """
    def __init__(self, path, language):
        super().__init__(path)
        self.language = language


class ExecutableFile(BaseFile):
    """
    Executable file class for use in sandbox directory.
    """
    def execute_program(self, input_file, output_file):
        """
        Execute the program using the given input file as STDIN, and the
        output file as STDOUT.
        """
        with (input_file or input_file.open()) as fin, \
             (output_file or output_file.open('w')) as fout as:
            subprocess.run([self.path], stdin=fin, stdout=fout)


class WrappedExecutableFile(ExecutableFile):
    """
    Wrapped executableFile class for use in sandbox directory.
    """
    def __init__(self, path, base_exec):
        super().__init__(path)
        self.base_exec = base_exec

    def execute_program(self, input_file, output_file):
        """
        Execute the program using the given input file as STDIN, and the
        output file as STDOUT (None to skip).
        """
        with (input_file or input_file.open()) as fin, \
             (output_file or output_file.open('w')) as fout as:
            subprocess.run([self.base_exec, self.path], stdin=fin, stdout=fout)


def CheckerFile(BaseFile):
    """
    Checker script file class for use in sandbox directory.
    """
    def check_result(self, input_file, output_file, solution_file):
        """
        Check if the solution is correct.
        """
