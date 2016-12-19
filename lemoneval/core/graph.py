# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

import operator
import random
from typing import Optional, Dict
from numbers import Number


class BaseTestNode(object):
    """
    The base class for all test nodes. It overloads many different operators
    so that test cases can be composed to create a more complex test suite
    structure.
    """
    def __init__(self):
        # List of nodes which should be evaluated before this node.
        self.dependencies = []  # type: List[BaseTestNode]

    def evaluate(self,
                 data: Optional[Dict] = None,
                 history: Optional[Dict] = None):
        # data: a mapping from any identifier to any data
        # history: a mapping from each computed node to score
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


class ConstantNode(BaseTestNode):
    """
    The node which always evaluate to a constant.
    """
    def __init__(self, value):
        self.dependencies = []
        self.value = value

    def evaluate(self,
                 data: Optional[Dict] = None,
                 history: Optional[Dict] = None):
        """
        Return the constant as the score.
        """
        return self.value


class OperatorNode(BaseTestNode):
    """
    A node which represents an operation on one or more test nodes.
    """
    def __init__(self, op, *args):
        self.dependencies = []
        self.op = op
        for arg in args:
            if isinstance(arg, BaseTestNode):
                self.dependencies.append(arg)
            elif isinstance(arg, Number):
                self.dependencies.append(ConstantNode(arg))
            else:
                raise TypeError('Unsupported type in graph.')

    def evaluate(self,
                 data: Optional[Dict] = None,
                 history: Optional[Dict] = None):
        """
        Assuming that all dependencies are pre-computed, fetch all those
        scores from the history then apply the operation.
        """
        subscores = [ history[precursor] for precursor in self.dependencies ]
        return self.op(*subscores)


class RandomScoreNode(BaseTestNode):
    """
    A node which represents a random score.
    """
    def __init__(self, score, threshold=.5):
        self.dependencies = []
        self.score = score
        self.threshold = threshold

    def evaluate(self,
                 data: Optional[Dict] = None,
                 history: Optional[Dict] = None):
        """
        Random whether a full score should be returned.
        """
        if random.random() < self.threshold:
            return self.score
        else:
            return 0


class SimpleTestNode(BaseTestNode):
    """
    A node which represents a test.
    """
    def __init__(self, score, question_id, solution):
        self.dependencies = []
        self.score = score
        self.question_id = question_id
        self.solution = solution

    def evaluate(self,
                 data: Optional[Dict] = None,
                 history: Optional[Dict] = None):
        """
        Check if the answer to the given question (identified by its ID)
        matches the expected solution.
        """
        if data[self.question_id] == self.solution:
            return self.score
        else:
            return 0
