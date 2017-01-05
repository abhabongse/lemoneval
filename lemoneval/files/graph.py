# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

import os
from typing import Optional, Dict
from .sandbox import TemporarySandbox
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
        self.score = score
        self.func_id = func_id
        self.checker = checker
        self.input_fname = input_fname
        self.solution_fname = solution_fname

        assert(os.path.isabs(input_fname)
               and os.path.exists(input_fname))
        assert(os.path.isabs(solution_fname)
               and os.path.exists(solution_fname))

    def evaluate(self,
                 data: Optional[Dict] = None,
                 history: Optional[Dict] = None):

        # Create a temporary sandbox for intermediate file storage.
        with TemporarySandbox() as sb:
            input_fname = sb.get_file_from_src(self.input_fname, 'input.txt')
            output_fname = sb.get_empty_file_location('output.txt')

            # Obtain the callable function and run
            if data is not None and self.func_id in data:
                func = data[self.func_id]
                try:
                    func(input_fname, output_fname)
                except:
                    return 0
                else:
                    solution_fname = sb.get_file_from_src(
                        self.solution_fname, 'solution.txt'
                        )
                    return self.checker(
                        self.score, input_fname, output_fname, solution_fname
                        )
            else:
                return 0
