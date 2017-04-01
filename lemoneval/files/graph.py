# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
"""Test node components extension for tests stored in files."""

from numbers import Number
import pathlib
import os
import tempfile
from typing import Optional, Dict
from .checker import BaseChecker
from .sandbox import TemporarySandbox
from .util import sanitize_file
from ..core.graph import BaseNode
from ..core.descriptors import TypedDataDescriptor


class FileProgramTestNode(BaseNode):
    """A test node which uses provided program to evaluate some input data
    where input and solution hint files are stored on filesystem storage.

    A program to this test node is a callable external data identified by the
    `program_id` dictionary key.

    The evaluation of the output by the program is done via `checker` object.

    Attributes:
        full_score: Score of this test node
        program_id: Dictionary key to a callable program in external data
        checker: Object whose callable checks if the output is correct based
            on the input and solution clue
        input_fname: Path to input data
        solution_fname: Path to solution hint data
        time_limit: Seconds before timeout (default: 60 seconds)

    """
    full_score = TypedDataDescriptor(Number)
    checker = TypedDataDescriptor(BaseChecker)
    input_fname = TypedDataDescriptor(pathlib.Path)
    solution_fname = TypedDataDescriptor(pathlib.Path)
    time_limit = TypedDataDescriptor(Number, lambda x: x > 0)

    def __init__(self, full_score, program_id, checker, input_fname,
                 solution_fname, time_limit=60):
        input_fname = sanitize_file(input_fname)
        solution_fname = sanitize_file(solution_fname)

        self.full_score = full_score
        self.program_id = program_id
        self.checker = checker
        self.input_fname = input_fname
        self.solution_fname = solution_fname
        self.time_limit = time_limit

    def evaluate(self, result, data):
        # Create a temporary sandbox for intermediate file storage.
        with TemporarySandbox() as sandbox:
            # Obtain progran from external data
            try:
                program = data[self.program_id]
            except KeyError:
                result[self].messages['lookup_error'] = "program not provided"
                return
            # Execute the program
            input_fname = sandbox.copy_file(self.input_fname, 'input.txt')
            output_fname = sandbox.get_file_location('output.txt')
            try:
                program(input_fname, output_fname)
            except:
                result[self].messages['runtime_error'] = "runtime error"
                return
            # Check the output
            solution_fname = sandbox.copy_file(
                self.solution_fname, 'solution.txt'
                )
            self.checker(
                result[self], self.full_score, input_fname, output_fname,
                solution_fname
                )
