# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
import operator
import os.path

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

    def evaluate(self, executable, check_script, *, prefix_spaces=''):
        """
        Evaluate the score of this test structure.
        """
        return 0, ''


class TestCaseConstant(BaseTestCase):
    """
    A class for test case which does not contain the actual test but
    contain a constant.
    """
    def __init__(self, value):
        self.value = value

    def evaluate(self, executable, check_script, *, prefix_spaces=''):
        """
        Use the stored constant as the score.
        """
        message = '{}{}'.format(prefix_spaces, self.value)
        return self.value, message


class TestCaseOperation(BaseTestCase):
    """
    A class for test case group whose score is built up from two smaller
    test cases.
    """
    def __init__(self, op, *expressions, name=None):
        self.op = op
        self.name = name or op.__name__
        self.expressions = [
            atom if isinstance(atom, BaseTestCase) else TestCaseConstant(atom)
            for atom in expressions
        ]

    def evaluate(self, executable, check_script, *, prefix_spaces=''):
        """
        Evaluate the score of this test structure.
        """
        scores = []
        messages = []
        for atom in self.expressions:
            score, message = atom.evaluate(
                executable, check_script,
                prefix_spaces=prefix_spaces + '  '
            )
            scores.append(score)
            messages.append(message)
        computed_score = self.op(*scores)
        flattened_message = '{}Applying "{}" on the following\n{}'.format(
            prefix_spaces, self.name, '\n'.join(messages)
        )
        return computed_score, flattened_message

    @staticmethod
    def sum(*expressions):
        """
        Special sum operator for test cases structure.
        """
        sum_op = lambda *args: sum(args)
        sum_op.__name__ = 'sum'
        return TestCaseOperation(sum_op, *expressions)

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
    def __init__(self, input_file, solution_file, score_limit, name=None):
        # TODO: check file exists and is absolute path
        self.input_file = input_file
        self.solution_file = solution_file
        self.score_limit = score_limit
        self.name = name or os.path.splitext(os.path.basename(input_file))[0]

    def evaluate(self, executable, check_script, *, prefix_spaces=''):
        """
        Evaluate the score of this test case.
        """
        # TODO: implement me
        import random
        score = random.randint(0, self.score_limit)
        message = '{}{}/{} [{}] from test {}'.format(
            prefix_spaces, score, self.score_limit, 'correct', self.name
        )
        return score, message
