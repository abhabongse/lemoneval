# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

import operator
import random
from .graph import BaseTestNode, ConstantNode, OperatorNode

class BaseEvaluator(object):
    """
    Evaluate test graph with data to obtain the result.
    """
    def __init__(self, graph):
        """
        Initialize the evaluator with a test graph.
        """
        self.graph = graph

    def run(self, data):
        """
        Process the data to compute the score with the stored test graph.
        """
        # TODO: make sure that parts of code is injectable so that
        # some reporting functionality could work
        computed_node_scores = {}

        def traverse(node):
            # Check if the node has ever been visited
            if node in computed_node_scores:
                if computed_node_scores[node] is None:
                    raise ValueError('Test graph should not contain a cycle.')
                else:
                    return  # no need to recompute everything again
            computed_node_scores[node] = None

            # Check the node types and process accordingly
            if isinstance(node, ConstantNode):
                score = node.value
            elif isinstance(node, OperatorNode):
                subscores = []
                for child in node.children:
                    traverse(child)  # traverse down the tree
                    subscores.append(computed_node_scores[child])
                score = node.op(*subscores)
            elif isinstance(node, BaseTestNode):
                score = node.evaluate(data)
            else:
                raise ValueError('Test graph should not contain invalid nodes.')

            # Store the computed score
            computed_node_scores[node] = score

        # Traverse from the root and obtain the final score
        traverse(self.graph)
        final_score = computed_node_scores[self.graph]
        return final_score
