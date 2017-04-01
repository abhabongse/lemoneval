#!/usr/bin/env python3
# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

import pathlib
from lemoneval import (
    ProgramTestNode, FileProgramTestNode, WordChecker, node_min,
    chains
    )

check_script = WordChecker()
this_dir = pathlib.Path(__file__).absolute().parent
program_tests = [
    FileProgramTestNode(10, 'program', check_script,
                        this_dir.joinpath(f'test-{i}.in'),
                        this_dir.joinpath(f'test-{i}.sol'))
    for i in ('1', '2', '3a', '3b')
]
written_tests = [
    # The question id is the input, and the expected output is always '1'.
    ProgramTestNode(10, 'function', f'q{i}', '1')
    for i in (1, 2, 3)
    ]

ROOT_TEST = (
    program_tests[0] + program_tests[1]
    # Both '3a' and '3b' must be solved to obtain the score
    + node_min(program_tests[2], program_tests[3])
    # Score awarding is contingent to the previous correct answer.
    + chains(*written_tests)
    )
