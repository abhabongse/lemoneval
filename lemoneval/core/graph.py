# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
"""Test node components to construct a more complex test suite structure.

This module is self-contained and provides a building block to construct more
complicated test suites.

"""
from collections.abc import Callable
import operator
import random
from numbers import Number
from .descriptors import TypedDataDescriptor


class BaseNode(object):
    """Base class for all test nodes.

    It overloads many different operators so that test cases can be composed
    to create a more complex test suite tree structure.

    """
    def evaluate(self, result, data):
        """Evaluate this test node with the given data.

        This method should never be called directed. It is intended to be
        called when the `Result` object is constructed.

        Subclass of `BaseNode` is expected to override this method.

        Args:
            data: External data to evaluate this test node.
            dscores: Mapping from dependent test nodes to evaluated scores.

        Side-effect:
            This method should populate attributes of data[self] such as
            `success`, `scores`, and `messages`.

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
            TypeError: If conditions under Return section is not satisfied

        """
        if isinstance(value, BaseNode):
            return value
        elif isinstance(value, Number):
            return ConstantNode(value)
        else:
            raise TypeError("unsupported type for {value!r} in test graph")


class ConstantNode(BaseNode):
    """A constant test score node.

    Attributes:
        full_score: Constant score value

    """
    full_score = TypedDataDescriptor(Number)

    def __init__(self, full_score):
        self.full_score = full_score

    def evaluate(self, result, data):
        result[self].success = 1
        result[self].score = self.full_score


class OperatorNode(BaseNode):
    """An operator node applying math operations on zero or more test nodes.

    The evaluated score of this node is the result of applying the operator
    to scores of all evaluated operand.

    Attributes:
        op: Function which computes the aggregate scores based on scores
            of each node in the operand
        operand (`list` of `BaseNode`): Sequence of nodes whose scores
            will be combined through the specified function `op`

    """
    op = TypedDataDescriptor(Callable)

    def __init__(self, op, *args):
        self.op = op
        self.operand = [ self.make_node(arg) for arg in args ]

    def evaluate(self, result, data):
        subscores = [ result[op_node].score for op_node in self.operand ]
        result[self].success = 1
        result[self].score = self.op(*subscores)


class TernaryIfNode(BaseNode):
    """Special ternary if operator for three test nodes.

    This node evaluates to `then_expr` if the evaluation of `if_expr` is True
    as judged by `bool()`. Otherwise, this node evaluates to `else_expr`.

    Note that the other branch will not be evaluated (at least not directly).

    Attributes:
        if_expr: An conditional expression.
        then_expr: A then-branch expression.
        else_expr: An else-branch expression.

    """
    def __init__(self, if_expr, then_expr, else_expr):
        self.if_expr = self.make_node(if_expr)
        self.then_expr = self.make_node(then_expr)
        self.else_expr = self.make_node(else_expr)

    def evaluate(self, result, data):
        if result[self.if_expr].score:
            result[self].success = result[self.then_expr].success
            result[self].score = result[self.then_expr].score
        else:
            result[self].success = result[self.else_expr].success
            result[self].score = result[self.else_expr].score


class LotteryNode(BaseNode):
    """A lottery node that awards score with some probability.

    Attributes:
        full_score: Score for this test node
        threshold: Probability that full score is obtained, as opposed to 0

    """
    full_score = TypedDataDescriptor(Number)
    threshold = TypedDataDescriptor(Number, lambda x: 0 <= x <= 1)

    def __init__(self, full_score, threshold=.5):
        self.full_score = full_score
        self.threshold = threshold

    def evaluate(self, result, data):
        sample = random.random()
        if sample < self.threshold:
            result[self].success = 1
            result[self].score = self.full_score
        result[self].messages['sample'] = sample


class AnswerOnlyTestNode(BaseNode):
    """A test node which looks up an answer from the external data.

    An answer to this test node is an external data identified by the
    `answer_id` dictionary key.

    The answer is considered correct if the given `predicate` evaluates the
    answer to `True`. If `predicate` is not callable, it turns itself into
    an equality check.

    Attributes:
        full_score: Score for this test node
        answer_id: Dictionary key to an answer in external data
        predicate: Boolean function which takes in the answer from external
            data and evaluates its correctness. If not callable, then it turns
            itself into an equality check callable.

    """
    full_score = TypedDataDescriptor(Number)
    predicate = TypedDataDescriptor(Callable)

    def __init__(self, full_score, answer_id, predicate):
        self.full_score = full_score
        self.answer_id = answer_id
        if callable(predicate):
            self.predicate = predicate
        else:
            self.predicate = lambda x: (x == predicate)

    def evaluate(self, result, data):
        try:
            answer = data[self.answer_id]
        except KeyError:
            result[self].messages['lookup_error'] = "answer not provided"
            return
        if self.predicate(answer):
            result[self].success = 1
            result[self].score = self.full_score
        result[self].messages['answer'] = answer


class ProgramTestNode(BaseNode):
    """A test node which uses provided program to evaluate some input data.

    A program to this test node is a callable external data identified by the
    `program_id` dictionary key.

    The program is considered correct if the given `predicate` evaluates the
    output of the program given `test_input` as the program input. If
    `predicate` is not callable, it turns itself into an equality check.

    Attributes:
        full_score: Score of this test node
        program_id: Dictionary key to a callable program in external data
        test_input: Input data.
        predicate: Boolean function which takes in the output from the program
            from the external data given the `test_input` as the input, and
            evaluates its correctness. If not callable, then it turns itself
            into an equality check callable.

    """
    full_score = TypedDataDescriptor(Number)
    predicate = TypedDataDescriptor(Callable)

    def __init__(self, full_score, program_id, test_input, predicate):
        self.full_score = full_score
        self.program_id = program_id
        self.test_input = test_input
        if callable(predicate):
            self.predicate = predicate
        else:
            self.predicate = lambda x: (x == predicate)

    def evaluate(self, result, data):
        try:
            program = data[self.program_id]
        except KeyError:
            result[self].messages['lookup_error'] = "program not provided"
            return
        try:
            test_output = program(self.test_input)
        except:
            result[self].messages['runtime_error'] = "runtime error"
            return
        if self.predicate(test_output):
            result[self].success = 1
            result[self].score = self.full_score
        result[self].messages['output'] = test_output


#######################
## Special functions ##
#######################

def chains(first, second, *rest):
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
        new_first = second
        new_second, *new_rest = rest
        next_node = chains(new_first, new_second, *new_rest)
    else:
        next_node = second
    return TernaryIfNode(first, first + next_node, 0)


def node_sum(expressions):
    """Special sum operator for test nodes.

    Args:
        expressions: Sequence of test nodes, part of summand

    Returns:
        New test node which is the sum of all expressions

    """
    sum_op = lambda *exp: sum(exp)
    return OperatorNode(sum_op, *expressions)


def node_max(first, *rest):
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


def node_min(first, *rest):
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
