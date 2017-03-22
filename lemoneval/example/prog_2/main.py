#!/usr/bin/env python3
# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

import importlib.util
import pathlib
from lemoneval import BaseResult, load_test, Executable

# Load test suite
this_dir = pathlib.Path(__file__).absolute().parent
tests = load_test(this_dir.joinpath('tests', 'config.py'))

##############
## SOLVER 1 ##
##############

# Load solver as executable
solver = Executable(this_dir.joinpath('solver.py'))
data = { 'program': solver }

# Run the program and obtain the result
result = BaseResult(tests, data)
assert(result.final_score == 20)
print('Should be 20:', result.final_score)

##############
## SOLVER 2 ##
##############

# Load wrong_solver as executable
this_dir = pathlib.Path(__file__).absolute().parent
solver = Executable(this_dir.joinpath('wrong_solver.py'))
data = { 'program': solver }

# Run the program and obtain the result
result = BaseResult(tests, data)
assert(result.final_score == 10)
print('Should be 10:', result.final_score)