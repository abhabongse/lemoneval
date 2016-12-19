#!/usr/bin/env python3
# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from lemoneval import SimpleTestNode, Evaluator

tests = [ SimpleTestNode(20, i, str(i)) for i in range(1, 6) ]
test_suite = sum(tests)
evaluator = Evaluator(test_suite)
guesses = { i: input('Guess: ') for i in range(1, 6) }
grading = evaluator.run(guesses)
print(grading.final_score)
