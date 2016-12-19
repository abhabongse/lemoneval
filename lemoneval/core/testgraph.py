# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
"""Test node components to construct a more complex test suite structure.

This module is self-contained and provides a building block to construct more
complicated test suites.
"""

import operator
import random
from typing import Optional, Dict
from numbers import Number

class BaseNode(object):
    """Base class for all test nodes.

    It overloads many different operators
    so that test cases can be composed to create a more complex test suite
    tree structure.

    Attributes:
        dependencies (`list` of `BaseNode`): Nodes which should be evaluated
            before this node.

    """
    def __init__(self):
        self.dependencies = []  # type: List[BaseNode]

    def evaluate(self,
                 data: Optional[Dict] = None,
                 history: Optional[Dict] = None):
        """Evaluate this test node with the given data.

        This method assumes that all nodes from `dependencies` attribute
        have already been evaluated and scores are already obtained.

        Subclass of `BaseNode` is expected to override this method.

        Args:
            data: External data to evaluate this test node.
            history: Mapping from dependent test nodes to evaluated scores.

        Returns:
            The computed score.

        """
        raise NotImplementedError

    def run(self, data: Optional[Dict] = None) -> ('GradingResult'):
        """Evaluate the entire test suite with the given data.

        Using this node as the root of the test suite tree structure,
        evaluate the entire test suite tree with the given data.

        Args:
            data: External data to evaluate this test node

        Returns:
            An object of class `GradingResult` containing information about
            the grading result.

        """
        return GradingResult(self, data)

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


class ConstantNode(BaseNode):
    """A node which represents a constant value.

    When this node is evaluated, the constant is returned as the score.

    Attributes:
        value: Constant value

    """
    def __init__(self, value):
        self.dependencies = []
        self.value = value

    def evaluate(self,
                 data: Optional[Dict] = None,
                 history: Optional[Dict] = None):
        return self.value


class OperatorNode(BaseNode):
    """A node which represents an operation on zero or more test nodes.

    When this node is evaluated, the aggregrate scores is returned based
    on scores of nodes in dependencies.

    Attributes:
        dependencies (`list` of `BaseNode`): Sequence of nodes whose scores
            will be combined through the specified function `op`.
        op: Function which computes the aggregrate scores based on scores
            of each node in dependencies

    """
    def __init__(self, op, *args):
        self.dependencies = []
        self.op = op
        for arg in args:
            if isinstance(arg, BaseNode):
                self.dependencies.append(arg)
            elif isinstance(arg, Number):
                self.dependencies.append(ConstantNode(arg))
            else:
                raise TypeError('Unsupported type in graph.')

    def evaluate(self,
                 data: Optional[Dict] = None,
                 history: Optional[Dict] = None):
        subscores = [ history[precursor] for precursor in self.dependencies ]
        return self.op(*subscores)


class LotteryNode(BaseNode):
    """A node which represents a random score.

    Attributes:
        dependencies (`list` of `BaseNode`): Sequence of nodes whose scores
            will be combined through the specified function `op`.
        score: Score for this test node.
        threshold: Probability that full score is obtained, as opposed to 0.
    """
    def __init__(self, score, threshold=.5):
        self.dependencies = []
        self.score = score
        self.threshold = threshold

    def evaluate(self,
                 data: Optional[Dict] = None,
                 history: Optional[Dict] = None):
        sample = random.random()
        if sample < self.threshold:
            return self.score
        else:
            return 0


class SimpleTestNode(BaseNode):
    """A node which represents a simple test.

    It uses `test_id` as a key to obtain the external data and check if it
    passes the specified `predicate`.

    Attributes:
        dependencies (`list` of `BaseNode`): Sequence of nodes whose scores
            will be combined through the specified function `op`.
        score: Score for this test node.
        test_id: Key of external `data` dictionary.
        predicate: Boolean function which checks the input from external data.

    """
    def __init__(self, score, test_id, predicate):
        self.dependencies = []
        self.score = score
        self.test_id = test_id
        self.predicate = predicate

    def evaluate(self,
                 data: Optional[Dict] = None,
                 history: Optional[Dict] = None):
        if self.test_id in data and self.predicate(data[self.test_id]):
            return self.score
        else:
            return 0


class GradingResult(object):
    """Object which stores a evaluation history of a test suite.

    Whenever a test is run with `run` method of test nodes, this object
    is created to store all scores of each test in the tree and the final
    score is also computed.

    Attributes:
        graph: Root of trees carrying all test nodes.
        data: External data for test evaluations.
        computed_node_scores: Dictionary mapping from nodes to computed scores.
        final_score: Final score of test suite.

    """
    def __init__(self, graph: BaseNode, data: Optional[Dict] = None):
        self.graph = graph
        self.data = data
        self.computed_node_scores = {}

        # Traverse the node to evaluate the data.
        self.traverse(graph)
        self.final_score = self.computed_node_scores[graph]

    def traverse(self, node: BaseNode):
        """Evaluate and obtain scores for the specified node.

        Args:
            node: Current test node in consideration.

        Raises:
            ValueError: If the test suite tree contains a cycle.
        """
        # Check if the node has ever been visited
        if node in self.computed_node_scores:
            if self.computed_node_scores[node] is None:
                raise ValueError('Test graph should not contain cycles.')
            else:
                return  # no need to recompute this node again

        # Temporary value while the score is waited to be computed
        self.computed_node_scores[node] = None

        # Compute all dependencies first
        for precursor in node.dependencies:
            self.traverse(precursor)

        # Evaluate the node itself and store the score
        score = node.evaluate(self.data, self.computed_node_scores)
        self.computed_node_scores[node] = score
