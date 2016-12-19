# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

import operator
import random
from typing import Optional, Dict
from .graph import BaseTestNode, ConstantNode, OperatorNode

class Evaluator(object):
    """
    Evaluate test graph with data to obtain the result.
    """
    def __init__(self, graph: BaseTestNode):
        """
        Initialize the evaluator with a test graph.
        """
        self.graph = graph

    def run(self, data: Optional[Dict] = None) -> 'Grading':
        """
        Process the data to compute the score with the stored test graph.
        """
        return Grading(self, data)


class Grading(object):
    """
    An evaluation instance of Evaluator on a given data.
    """
    def __init__(self, evaluator: Evaluator, data: Optional[Dict] = None):
        self.evaluator = evaluator
        self.data = data
        # This stores a mapping from each computed node to score
        self.computed_node_scores = {}
        # Traverse the node to evaluate the data.
        self.traverse(evaluator.graph)
        self.final_score = self.computed_node_scores[evaluator.graph]

    def traverse(self, node: BaseTestNode):
        # Check if the node has ever been visited
        if node in self.computed_node_scores:
            if self.computed_node_scores[node] is None:
                raise ValueError('Test graph should not contain cycles.')
            else:
                return  # no need to recompute this node again

        # Compute all dependencies first
        for precursor in node.dependencies:
            self.traverse(precursor)

        # Evaluate the node itself and store the score
        score = node.evaluate(self.data, self.computed_node_scores)
        self.computed_node_scores[node] = score
