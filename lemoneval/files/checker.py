# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

import filecmp
import os
import subprocess
from itertools import zip_longest
from decimal import Decimal


class BaseChecker(object):
    """Compares the output and solution files, byte-by-byte."""

    def __call__(self, full_score, input_fname, output_fname, solution_fname):
        """Use the solution file to check if the output it correct.

        Args:
            full_score: Maximum score if the output is correct
            input_fname: Path to input file
            output_fname: Path to output file
            solution_fname: Path to solution file

        Returns:
            `full_score` if the output is correct, 0 otherwise

        """
        if self.check_answer(input_fname, output_fname, solution_fname):
            return full_score
        else:
            return 0

    def check_answer(self, input_fname, output_fname, solution_fname):
        """Compare output and solution files to see if they are identical.

        Args:
            input_fname: Path to input file
            output_fname: Path to output file
            solution_fname: Path to solution file

        Returns:
            Boolean whether the output and solution files are identical

        """
        filecmp.clear_cache()
        return filecmp.cmp(output_fname, solution_fname, shallow=False)


class WordChecker(BaseChecker):
    """Compare the output and solution files, word-by-word."""

    def check_answer(self, input_fname, output_fname, solution_fname):
        """Compare output and solution files to see if they are word-by-word.

        Words in each line must be exactly the same, with one or more blank
        spaces separating each word in the same line. The amount of spaces
        may differ in both files.

        Args:
            input_fname: Path to input file
            output_fname: Path to output file
            solution_fname: Path to solution file

        Returns:
            Boolean whether the output and solution files are identical

        """
        def word_stream(fobj):
            for line in fobj:
                for word in line.split():
                    yield word
                yield '\n'

        with open(output_fname) as fout, open(solution_fname) as fsol:
            stream_a = word_stream(fout)
            stream_b = word_stream(fsol)
            return all(
                word_a == word_b
                for (word_a, word_b) in zip_longest(stream_a, stream_b)
                )


class ExternalChecker(BaseChecker):
    """Check the solution using external script.

    Attributes:
        script_path: Path to script which accepts four command-lind parameters,
            the full score, input file, output file, and solution file.

    """
    def __init__(self, script_path):
        self.script_path = script_path

    def __call__(self, full_score, input_fname, output_fname, solution_fname):
        """Use the solution file to check if the output it correct.

        Args:
            full_score: Maximum score if the output is correct
            input_fname: Path to input file
            output_fname: Path to output file
            solution_fname: Path to solution file

        Returns:
            `full_score` if the output is correct, 0 otherwise

        """
        result = subprocess.run(
            [self.script_path, full_score, input_fname, output_fname,
             solution_fname], stdout=subprocess.PIPE
            )
        stdout_lines = result.stdout.split('\n')
        return Decimal(stdout_lines[0])
