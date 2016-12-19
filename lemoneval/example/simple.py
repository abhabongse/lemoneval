#!/usr/bin/env python3
# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from lemoneval import BaseNode, SimpleTestNode, LotteryNode

def is_equal(target_int):
    """
    Generates a predicate which checks if a given value matches the
    pre-specified target.
    """
    def predicate(value):
        try:
            return int(value) == target_int
        except ValueError:
            return False
    return predicate


# Generate a few tests and combine them
tests = [ SimpleTestNode(20, i, is_equal(i)) for i in range(1, 6) ]
tests.append(LotteryNode(50, 0.5))
test_suite = sum(tests)  # type: BaseNode

# Obtain guesses from input prompt
guesses = { i: input('Guess: ') for i in range(1, 6) }

# Evaluate all guesses and obtain final score
grading = test_suite.run(guesses)
print(grading.final_score)
