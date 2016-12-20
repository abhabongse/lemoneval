# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
"""Computes the grading result of a test graph using given data.

This module relies heavily on the `graph` module. `BaseResult` takes in
a constructed test graph and a dictionary of data, and attempts to evaluate
all test nodes in order to compute the final score. Intermediate results and
computational history may be kept within the object.

"""

from typing import Optional, Dict
from .graph import BaseNode

class BaseResult(object):
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
        self.data = data if data else {}
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
