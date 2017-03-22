# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
"""Test node components to construct a more complex test suite structure.

This module is self-contained and provides a building block to construct more
complicated test suites.

"""

import operator
import random
from typing import Optional, Dict, Sequence
from numbers import Number

class BaseNode(object):
    """Base class for all test nodes.

    It overloads many different operators so that test cases can be composed
    to create a more complex test suite tree structure.

    Attributes:
        dependencies (`list` of `BaseNode`): Nodes which should be evaluated
            before this node.

    """
    dependencies: Sequence['BaseNode'] = []

    def evaluate(self,
                 data: Optional[Dict] = None,
                 dscores: Optional[Dict] = None):
        """Evaluate this test node with the given data.

        This method assumes that all nodes from `dependencies` attribute
        have already been evaluated and scores are already obtained.

        Subclass of `BaseNode` is expected to override this method.

        Args:
            data: External data to evaluate this test node.
            dscores: Mapping from dependent test nodes to evaluated scores.

        Returns:
            The computed score.

        """
        raise NotImplementedError

    def __add__(self, other):
        return OperatorNode(operator.add, self, other)
    def __radd__(self, other):
        return OperatorNode(operator.add, other, self)

    def __sub__(self, other):
        return OperatorNode(operator.sub, self, other)
    def __rsub__(self, other):
        return OperatorNode(operator.sub, other, self)

    def __mul__(self, other):
        return OperatorNode(operator.mul, self, other)
    def __rmul__(self, other):
        return OperatorNode(operator.mul, other, self)

    def __truediv__(self, other):
        return OperatorNode(operator.truediv, self, other)
    def __rtruediv__(self, other):
        return OperatorNode(operator.truediv, other, self)

    def __floordiv__(self, other):
        return OperatorNode(operator.floordiv, self, other)
    def __rfloordiv__(self, other):
        return OperatorNode(operator.floordiv, other, self)

    def __mod__(self, other):
        return OperatorNode(operator.mod, self, other)
    def __rmod__(self, other):
        return OperatorNode(operator.mod, other, self)

    def __pow__(self, other):
        return OperatorNode(operator.pow, self, other)
    def __rpow__(self, other):
        return OperatorNode(operator.pow, other, self)

    def __lshift__(self):
        return OperatorNode(operator.lshift, self, other)
    def __rlshift__(self):
        return OperatorNode(operator.lshift, other, self)

    def __rshift__(self, other):
        return OperatorNode(operator.rshift, self, other)
    def __rrshift__(self, other):
        return OperatorNode(operator.rshift, other, self)

    def __and__(self, other):
        return OperatorNode(operator.and_, self, other)
    def __rand__(self, other):
        return OperatorNode(operator.and_, other, self)

    def __xor__(self, other):
        return OperatorNode(operator.xor, self, other)
    def __rxor__(self, other):
        return OperatorNode(operator.xor, other, self)

    def __or__(self, other):
        return OperatorNode(operator.or_, self, other)
    def __ror__(self, other):
        return OperatorNode(operator.or_, other, self)

    def __neg__(self):
        return OperatorNode(operator.neg, self)
    def __pos__(self):
        return OperatorNode(operator.pos, self)
    def __abs__(self):
        return OperatorNode(operator.abs, self)
    def __invert__(self):
        return OperatorNode(operator.inv, self)

    def make_node(self, value):
        """Convert a value into an instance of `BaseNode` subclass type.

        Args:
            value: Value to convert to an instance of `BaseNode` subclass.

        Returns:
            If `value` is already a `BaseNode`, it is returned as-is.
            If `value` is a number, it is wrapped inside `ConstantNode`
                and returned.

        Raises:
            TypeError: If conditions under Return section is not satisfied.

        """
        if isinstance(value, BaseNode):
            return value
        elif isinstance(value, Number):
            return ConstantNode(value)
        else:
            raise TypeError('Unsupported type in graph.')


class ConstantNode(BaseNode):
    """A node which represents a constant score.

    When this node is evaluated, the constant is returned as the score.

    Attributes:
        score: Constant score value

    """
    def __init__(self, score):
        self.score = score

    def evaluate(self, data: Optional[Dict] = None,
                 dependent_scores: Optional[Dict] = None):
        return self.score


class OperatorNode(BaseNode):
    """A node which represents an operation on zero or more test nodes.

    When this node is evaluated, the aggregate scores is returned based
    on scores of nodes in dependencies.

    Attributes:
        dependencies (`list` of `BaseNode`): Sequence of nodes whose scores
            will be combined through the specified function `op`.
        op: Function which computes the aggregate scores based on scores
            of each node in dependencies

    """
    def __init__(self, op, *args):
        self.dependencies = []
        self.op = op
        for arg in args:
            self.dependencies.append(self.make_node(arg))

    def evaluate(self, data: Optional[Dict] = None,
                 dscores: Optional[Dict] = None):
        subscores = [ dscores[prev] for prev in self.dependencies ]
        return self.op(*subscores)


class LotteryNode(BaseNode):
    """A node which represents a random score.

    Attributes:
        score: Score for this test node.
        threshold: Probability that full score is obtained, as opposed to 0.

    """
    def __init__(self, score, threshold=.5):
        self.score = score
        self.threshold = threshold

    def evaluate(self, data: Optional[Dict] = None,
                 dscores: Optional[Dict] = None):
        sample = random.random()
        if sample < self.threshold:
            return self.score
        else:
            return 0


class OutputPredicateTestNode(BaseNode):
    """A node which represents a simple answer-only test.

    Each question is identified by `test_id` which is incidentally the key to
    obtain the answers from external data. The answer is considered correct
    if `predicate` evaluates to `True` on the output.

    Attributes:
        score: Score for this test node.
        test_id: Key of external `data` dictionary which will be the input
            to the `predicate`.
        predicate: Boolean function which checks the input from external data.
            In case it is not callable, it turns into the equality check to
            the given predicate value.

    """
    def __init__(self, score, test_id, predicate):
        self.score = score
        self.test_id = test_id
        self.predicate = (
            predicate if callable(predicate) else lambda x: (x == predicate)
            )

    def evaluate(self, data: Optional[Dict] = None,
                 dscores: Optional[Dict] = None):
        if (data is not None
                and self.test_id in data
                and self.predicate(data[self.test_id])):
            return self.score
        else:
            return 0


class FunctionalPredicateTestNode(BaseNode):
    """A node which represents a simple functional test.

    An input will be provided to the callable function as designated by
    `func_id` key of the external data. The answer is considered correct
    if `predicate` evaluates to `True` on the output.

    Attributes:
        score: Score for this test node.
        func_id: Key of external `data` dictionary which will be the
            callable function which expects an input.
        test_input: Input data.
        predicate: Boolean function which checks the input from external data.
            It expects the output, the input

    """
    def __init__(self, score, func_id, test_input, predicate):
        self.score = score
        self.func_id = func_id
        self.test_input = test_input
        self.predicate = (
            predicate if callable(predicate) else lambda x: (x == predicate)
            )

    def evaluate(self, data: Optional[Dict] = None,
                 dscores: Optional[Dict] = None):
        if data is not None and self.func_id in data:
            # Obtain function and evaluate the test input
            func = data[self.func_id]
            try:
                output = func(self.test_input)
            except:
                passed = False  # function raises an exception
            else:
                passed = self.predicate(output)
            return self.score if passed else 0
        else:
            return 0


#######################
## Special functions ##
#######################

def ternary_if(if_expr, then_expr, else_expr) -> (OperatorNode):
    """Special ternary if operator for three test nodes.

    This node evaluates to `then_expr` if the evaluation of `if_expr` is True
    as judge by `bool()`. Otherwise, this node evaluates to `else_expr`.

    Note that both `then_expr` and `else_expr` are both evaluated internally
    regardless of the truth value of `if_expr`.

    Args:
        if_expr: An conditional expression.
        then_expr: A then-branch expression.
        else_expr: An else-branch expression.

    Returns:
        New test node which is the ternary if expression of those three tests.
    """
    ite_op = lambda i, t, e: t if i else e
    return OperatorNode(ite_op, if_expr, then_expr, else_expr)


def chains(first, second, *rest) -> (OperatorNode):
    """Chain of tests that each test is contingent to the previous ones.

    This node evaluates each test in sequence in a way that the evaluation of
    each test node is contingent to the successful evaluation of the previous
    test node. The total score will be the sum of scores up to the last
    successful evaluation of a test node.

    Args:
        first: First test node expression
        second: Second test node expression
        rest: Sequence of test node expression succeeding the second one

    Returns:
        New test node which is the sum of all nodes with the given contingency
        condition as described above.

    """
    if rest:
        new_first, new_second = second, rest.pop(0)
        next_node = contingent(new_first, new_second, rest)
    else:
        next_node = second
    # TODO: add check condition to see if the returned score is full score
    return ternary_if(new_first, new_first + next_node, 0)


def tsum(expressions) -> (OperatorNode):
    """Special sum operator for test nodes.

    Args:
        expressions: Sequence of test nodes, part of summand

    Returns:
        New test node which is the sum of all expressions

    """
    sum_op = lambda *exp: sum(exp)
    return OperatorNode(sum_op, *expressions)


def tmax(first, *rest) -> (OperatorNode):
    """Special max operator for test nodes.

    Args:
        first: Either a single expression or a sequence of expressions.
            For the latter case, `rest` must be empty (that is only one
            argument is allowed in the function).
        rest: Sequence of expressions, part of max argument.

    Returns:
        New test node which is the max of all expressions.

    """
    if rest:
        return OperatorNode(max, first, *rest)
    else:
        return OperatorNode(max, *first)


def tmin(first, *rest) -> (OperatorNode):
    """Special min operator for test nodes.

    Args:
        first: Either a single expression or a sequence of expressions.
            For the latter case, `rest` must be empty (that is only one
            argument is allowed in the function).
        rest: Sequence of expressions, part of min argument.

    Returns:
        New test node which is the min of all expressions.

    """
    if rest:
        return OperatorNode(min, first, *rest)
    else:
        return OperatorNode(min, *first)
