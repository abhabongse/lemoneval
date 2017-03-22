#!/usr/bin/env python3
# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

import pathlib
from lemoneval import FunctionalFileTestNode, WordChecker, tsum

check_script = WordChecker()
this_dir = pathlib.Path(__file__).absolute().parent
tests = [
    FunctionalFileTestNode(10, 'program', check_script,
                           this_dir.joinpath(f'test-{i}.in'),
                           this_dir.joinpath(f'test-{i}.sol'))
    for i in (1, 2)
    ]
ROOT_TEST = tsum(tests)
