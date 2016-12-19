#!/usr/bin/env python3
# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from lemoneval import BaseNode, SimpleTestNode

tests = [ SimpleTestNode(20, i, str(i)) for i in range(1, 6) ]
test_suite = sum(tests)  # type: lemoneval.BaseNode
guesses = { i: input('Guess: ') for i in range(1, 6) }
grading = test_suite.run(guesses)
print(grading.final_score)
