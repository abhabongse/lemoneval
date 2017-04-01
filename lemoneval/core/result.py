# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
"""Evaluates a test graph using given data and store the result.

This module relies heavily on the `graph` module. `Result` takes in a
constructed test acyclic graph and a dictionary of data, and attempts to
evaluate all test nodes in order to compute the final score (represented by)
the score in the root of the tree. Intermediate results and computational
history may be kept within `NodeResult` object within the attribute called
`processed_nodes`.

"""
from numbers import Number
from .graph import BaseNode
from .descriptors import TypedDataDescriptor


class Result(object):
    """Object which stores an evaluation history of the a test graph.

    Whenever a test graph is evaluted via `get_result` function, this object is
    created to store all scores of each test in the graph and the final score
    is also computed.

    Attributes:
        final_score: Final score of test suite

    Item Lookup:
        object[key]: Node result of the test node `key`.

    Hidden Attributes:
        _root: Root of a test graph carrying all test nodes
        _data: Dictionary of external data for test evaluations
        _processed_nodes: Dictionary of nodes already traversed and evaluated
        _final_score: Final score of test suite

    """
    _root = TypedDataDescriptor(BaseNode)
    _data = TypedDataDescriptor(dict)

    def __init__(self, root, data=None):
        self._root = root
        self._data = data or {}
        self._processed_nodes = {}
        self.process(root)  # process the root node
        self._final_score = self._processed_nodes[root].score

    @property
    def final_score(self):  # read-only
        """Final score of test suite"""
        return self._final_score

    def __getitem__(self, key):
        """Obtain the corresponding node result from a given node."""
        if key not in self._processed_nodes:
            self.process(key)
        if key not in self._processed_nodes:
            raise KeyError(f"cannot process test node {key!r}")
        return self._processed_nodes[key]

    def process(self, node):
        # Check if the node is processed or if we detect a cycles
        if node in self._processed_nodes:
            if self._processed_nodes[node]._completed:
                return  # skip since already processed
            else:
                raise ValueError("test graph should not contain cycles")

        # Temporary placeholder for processed node result
        self._processed_nodes[node] = NodeResult(self, node)

        # Evaluate the node itself using external and result object itself
        # It should populate the node result itself
        node.evaluate(self, self._data)
        self._processed_nodes[node]._completed = True


class NodeResult(object):
    """Simple object to store the result of evaluating each test node.

    Attributes:
        success: Number between 0 and 1 indicating whether the evaluation of
            the node is considered a success or not
        score: Numeric value representing score from evaluating the node
        messages: List of messages popped during evaluation

    Hidden Attributes:
        _host: `Result` object hosting this node result
        _node: Test node corresponding to this node result
        _completed: Boolean indicating whether the evaluation of the node is
            already completed or nto
        _success: Number between 0 and 1 indicating whether the evaluation of
            the node is considered a success or not
        _score: Numeric value representing score from evaluating the node
    """
    _success = TypedDataDescriptor(Number, lambda x: 0 <= x <= 1)
    _score = TypedDataDescriptor(Number)

    def __init__(self, host, node):
        self._host = host
        self._node = node
        self._completed = False
        self._success = 0
        self._score = 0
        self.messages = {}

    @property
    def success(self):
        """Number between 0 and 1 indicating whether the evaluation of the node
        is considered a success or not.
        """
        return self._success

    @success.setter
    def success(self, value):
        if self._completed:
            raise AttributeError("modifying evaluated node not allowed")
        self._success = value

    @property
    def score(self):
        """Score from evaluating the test node."""
        return self._score

    @score.setter
    def score(self, value):
        if self._completed:
            raise AttributeError('modifying evaluated node not allowed')
        self._score = value


def compute_result(root_test, data):
    """Evaluate `root_test` using the given `data`.

    Args:
        root_test: Root of test node graph
        data: Dictionary of keys mapping to data

    Returns:
        Result object containing the result of the evaluation of `root_test`

    """
    return Result(root_test, data)
