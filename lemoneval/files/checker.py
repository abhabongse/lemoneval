# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
"""Collections of checker script to check if the output file is correct.

Given a full score, an input file, an output, and a solution file (also called
a checker hint file), checker determines if the output file is correct given
the existence of input and solution files.

"""
from decimal import Decimal
import filecmp
from itertools import zip_longest
import os
import pathlib
import subprocess


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
            A tuple of `success` value and the obtained `score` where:
            `success` is a number between 0 and 1
            `score` is `full_score` or 0 depending on whether output is correct

        """
        input_fname = pathlib.Path(input_fname)
        output_fname = pathlib.Path(output_fname)
        solution_fname = pathlib.Path(solution_fname)

        if self.check_answer(input_fname, output_fname, solution_fname):
            return 1, full_score
        else:
            return 0, 0

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
            A tuple of `success` value and the obtained `score` which are the
            output in the first and second line reported by external script

        """
        result = subprocess.run(
            [self.script_path, full_score, input_fname, output_fname,
             solution_fname], stdout=subprocess.PIPE
            )
        tokens = result.stdout.split('\n', 2)
        return Decimal(tokens[0]), Decimal(tokens[1])
