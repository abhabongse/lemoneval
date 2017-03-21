# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

import pathlib
import os
import tempfile
from typing import Optional, Dict
from lemoneval.files.sandbox import TemporarySandbox
from lemoneval.core.graph import BaseNode


class FunctionalFileTestNode(BaseNode):
    """A node which runs a callable function against an input and check its
    output. Input and solution clue files are stored on filesystem storage.

    Attributes:
        score: Score for this test node.
        func_id: Key of external `data` dictionary which will be the
            callable function which expects an input filename and
            an output filename.
        checker: Object whose callable checks if the output is correct
            based on the input and solution clue.
        input_fname: Path to input file
        solution_fname: Path to solution clue file

    """
    def __init__(self, score, func_id, checker, input_fname, solution_fname):
        input_fname = pathlib.Path(input_fname)
        solution_fname = pathlib.Path(solution_fname)

        if not (input_fname.is_absolute() and input_fname.exists()):
            raise FileNotFoundError(f"Input file not exists: {input_fname}")
        if not (solution_fname.is_absolute() and solution_fname.exists()):
            raise FileNotFoundError(f"Solution file not exists: "
                                    f"{solution_fname}")

        self.score = score
        self.func_id = func_id
        self.checker = checker
        self.input_fname = input_fname
        self.solution_fname = solution_fname

    def evaluate(self, data: Optional[Dict] = None,
                 history: Optional[Dict] = None):

        # Create a temporary sandbox for intermediate file storage.
        with TemporarySandbox() as sandbox:
            input_fname = sandbox.copy_file(self.input_fname, 'input.txt')
            output_fname = sandbox.get_file_location('output.txt')

            # Obtain the callable function and run
            if data is None or self.func_id not in data:
                return 0
            func = data[self.func_id]
            try:
                func(input_fname, output_fname)
            except:
                return 0
            solution_fname = sandbox.copy_file(
                self.solution_fname, 'solution.txt'
                )
            return self.checker(
                self.score, input_fname, output_fname, solution_fname
                )
