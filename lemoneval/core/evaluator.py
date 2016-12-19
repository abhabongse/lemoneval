# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

import operator
import random
from typing import Optional, Dict
from .graph import BaseTestNode

class Grading(object):
    """
    An evaluation instance of Evaluator on a given data.
    """
    def __init__(self, graph: BaseTestNode, data: Optional[Dict] = None):
        self.graph = graph
        self.data = data
        # This stores a mapping from each computed node to score
        self.computed_node_scores = {}
        # Traverse the node to evaluate the data.
        self.traverse(graph)
        self.final_score = self.computed_node_scores[graph]

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
