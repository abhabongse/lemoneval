# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

import os
from typing import Optional, Dict
from .sandbox import TemporarySandbox
from lemoneval.core.graph import BaseNode


class EvaluateProgramNode(BaseNode):
    """A node which runs a program against an input and check its output.

    Attributes:
        score: Score for this test node.
        program_id: Key of external `data` dictionary which will store the
            main program to evaluate `input_fname` and produce the output
        check_script: Object whose callable compares the output to
            `solution_fname`
        input_fname: Path to input file
        solution_fname: Path to solution file

    """
    def __init__(self, score, program_id, check_script,
                 input_fname, solution_fname):
        self.score = score
        self.program_id = program_id
        self.check_script = check_script
        self.input_fname = input_fname
        self.solution_fname = solution_fname
        self.dependencies = []

        assert(os.path.isabs(input_fname)
               and os.path.exists(input_fname))
        assert(os.path.isabs(solution_fname)
               and os.path.exists(solution_fname))

    def evaluate(self,
                 data: Optional[Dict] = None,
                 history: Optional[Dict] = None):

        # Create a temporary sandbox for intermediate file storage
        with TemporarySandbox() as sandbox:
            input_fname = sandbox.get_file_from_src(
                self.input_fname, 'input.txt'
                )
            output_fname = sandbox.get_empty_file_location('output.txt')

            # Obtain the program and run
            program = data[self.program_id]
            exits_normally = program(input_fname, output_fname)

            # Check the output if it is good
            if exits_normally:
                solution_fname = sandbox.get_file_from_src(
                    self.solution_fname, 'solution.txt'
                    )
                obtained_score = self.check_script(
                    self.score, input_fname, output_fname, solution_fname
                    )
            else:
                obtained_score = 0

        # Return the score
        return obtained_score
