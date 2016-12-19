#!/usr/bin/env python3
# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from lemoneval import SimpleTestNode, BaseEvaluator

tests = [ SimpleTestNode(20, i, i) for i in range(1, 6) ]
test_suite = sum(tests)
evaluator = BaseEvaluator(test_suite)
score = evaluator.run({1: 2,  2: 3,  3: 3,  4: 2,  5: 5})
print(score)
