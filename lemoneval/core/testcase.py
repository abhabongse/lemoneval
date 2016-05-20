# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
import operator

class BaseTestCase(object):
    """
    A base class of all test cases. It overloads many different operators,
    so that test cases are composable to build up a structure.
    """
    name = ''  # Type of test case.

    def __add__(self, other):
        return TestCaseOperation(operator.add, self, other)
    def __sub__(self, other):
        return TestCaseOperation(operator.sub, self, other)
    def __mul__(self, other):
        return TestCaseOperation(operator.mul, self, other)
    def __truediv__(self, other):
        return TestCaseOperation(operator.truediv, self, other)
    def __floordiv__(self, other):
        return TestCaseOperation(operator.floordiv, self, other)
    def __mod__(self, other):
        return TestCaseOperation(operator.mod, self, other)
    def __pow__(self, other):
        return TestCaseOperation(operator.pow, self, other)
    def __lshift__(self):
        return TestCaseOperation(operator.lshift, self, other)
    def __rshift__(self, other):
        return TestCaseOperation(operator.rshift, self, other)
    def __and__(self, other):
        return TestCaseOperation(operator.and_, self, other)
    def __xor__(self, other):
        return TestCaseOperation(operator.xor, self, other)
    def __or__(self, other):
        return TestCaseOperation(operator.or_, self, other)

    def __radd__(self, other):
        return TestCaseOperation(operator.add, other, self)
    def __rsub__(self, other):
        return TestCaseOperation(operator.sub, other, self)
    def __rmul__(self, other):
        return TestCaseOperation(operator.mul, other, self)
    def __rtruediv__(self, other):
        return TestCaseOperation(operator.truediv, other, self)
    def __rfloordiv__(self, other):
        return TestCaseOperation(operator.floordiv, other, self)
    def __rmod__(self, other):
        return TestCaseOperation(operator.mod, other, self)
    def __rpow__(self, other):
        return TestCaseOperation(operator.pow, other, self)
    def __rlshift__(self):
        return TestCaseOperation(operator.lshift, other, self)
    def __rrshift__(self, other):
        return TestCaseOperation(operator.rshift, other, self)
    def __rand__(self, other):
        return TestCaseOperation(operator.and_, other, self)
    def __rxor__(self, other):
        return TestCaseOperation(operator.xor, other, self)
    def __ror__(self, other):
        return TestCaseOperation(operator.or_, other, self)

    def __neg__(self):
        return TestCaseOperation(operator.neg, self)
    def __pos__(self):
        return TestCaseOperation(operator.pos, self)
    def __abs__(self):
        return TestCaseOperation(operator.abs, self)
    def __invert__(self):
        return TestCaseOperation(operator.inv, self)

    def get_score(self):
        """
        Return the score of the test case.
        """
        return 0


class TestCaseOperation(BaseTestCase):
    """
    A class for test case group whose score is built up from two smaller
    test cases.
    """
    def __init__(self, op, *expressions):
        self.op = op
        self.name = op.__name__
        self.expressions = expressions

    def get_score(self):
        scores = [
            atom.get_score() if isinstance(atom, BaseTestCase) else atom
            for atom in self.expressions
        ]
        return self.op(*scores)

    @staticmethod
    def max(first, *rest):
        """
        Special max operator for test cases structure.
        """
        if rest:
            return TestCaseOperation(max, first, *rest)
        else:
            return TestCaseOperation(max, *first)

    @staticmethod
    def min(first, *rest):
        """
        Special min operator for test cases structure.
        """
        if rest:
            return TestCaseOperation(min, first, *rest)
        else:
            return TestCaseOperation(min, *first)


class SimpleTestCase(BaseTestCase):
    """
    A class for simple test case, with an input file, a solution file,
    and a score limit.
    """
    def __init__(self, value):
        self.value = value

    def get_score(self):
        return self.value
