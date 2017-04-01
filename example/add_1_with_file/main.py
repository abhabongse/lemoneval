#!/usr/bin/env python3
# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

import os
from lemoneval import (
    FileProgramTestNode, compute_result, WordChecker, node_sum
    )

check_script = WordChecker()
this_dir = os.path.dirname(os.path.abspath(__file__))

def generate_input_solution_fnames(number):
    """
    Generates a pair of input and solution file names in terms of absolute
    path in relation to the directory of this file, with the attached number.
    """
    input_fname = os.path.join(this_dir, f'{number}.in')
    solution_fname = os.path.join(this_dir, f'{number}.sol')
    return input_fname, solution_fname

def prompt_solver(input_fname, output_fname):
    """
    Opens the input file, display the question to the user and ask for an
    answer. Then save the answer to the output file.
    """
    with open(input_fname) as fin:
        question = (fin.readline()).strip()
    answer = input(f'{question} + 1 = ')
    with open(output_fname, 'w') as fout:
        print(answer, file=fout)
    return True  # indicating that everything is okay


# Generate a few tests and combine them.
tests = [
    FileProgramTestNode(10, 'program', check_script,
                           *generate_input_solution_fnames(i))
    for i in (1, 2)
    ]
test_suite = node_sum(tests)

# Solve the test and obtain the result.
data = { 'program': prompt_solver }
result = compute_result(test_suite, data)
print(result.final_score)