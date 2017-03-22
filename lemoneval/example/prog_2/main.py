#!/usr/bin/env python3
# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

import importlib.util
import pathlib
from lemoneval import BaseResult
from lemoneval.files.executable import Executable


# Load solver as executable
this_dir = pathlib.Path(__file__).absolute().parent
solver = Executable(this_dir.joinpath('solver.py'))
data = { 'program': solver }

# Load test suite
spec = importlib.util.spec_from_file_location(
    'progtest.prog_2', this_dir.joinpath('tests', 'config.py')
    )
testconfig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(testconfig)
test_suite = testconfig.ROOT_TEST

# Run the program and obtain the result
result = BaseResult(test_suite, data)
print(result.final_score)
