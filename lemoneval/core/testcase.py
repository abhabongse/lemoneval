# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
import operator
import os.path

class BaseTest(object):
    """
    A base class of all test cases. It overloads many different operators,
    so that test cases are composable to build up a structure.
    """
    name = ''  # Type of test case.

    def __add__(self, other):
        return TestOperation(operator.add, self, other)
    def __sub__(self, other):
        return TestOperation(operator.sub, self, other)
    def __mul__(self, other):
        return TestOperation(operator.mul, self, other)
    def __truediv__(self, other):
        return TestOperation(operator.truediv, self, other)
    def __floordiv__(self, other):
        return TestOperation(operator.floordiv, self, other)
    def __mod__(self, other):
        return TestOperation(operator.mod, self, other)
    def __pow__(self, other):
        return TestOperation(operator.pow, self, other)
    def __lshift__(self):
        return TestOperation(operator.lshift, self, other)
    def __rshift__(self, other):
        return TestOperation(operator.rshift, self, other)
    def __and__(self, other):
        return TestOperation(operator.and_, self, other)
    def __xor__(self, other):
        return TestOperation(operator.xor, self, other)
    def __or__(self, other):
        return TestOperation(operator.or_, self, other)

    def __radd__(self, other):
        return TestOperation(operator.add, other, self)
    def __rsub__(self, other):
        return TestOperation(operator.sub, other, self)
    def __rmul__(self, other):
        return TestOperation(operator.mul, other, self)
    def __rtruediv__(self, other):
        return TestOperation(operator.truediv, other, self)
    def __rfloordiv__(self, other):
        return TestOperation(operator.floordiv, other, self)
    def __rmod__(self, other):
        return TestOperation(operator.mod, other, self)
    def __rpow__(self, other):
        return TestOperation(operator.pow, other, self)
    def __rlshift__(self):
        return TestOperation(operator.lshift, other, self)
    def __rrshift__(self, other):
        return TestOperation(operator.rshift, other, self)
    def __rand__(self, other):
        return TestOperation(operator.and_, other, self)
    def __rxor__(self, other):
        return TestOperation(operator.xor, other, self)
    def __ror__(self, other):
        return TestOperation(operator.or_, other, self)

    def __neg__(self):
        return TestOperation(operator.neg, self)
    def __pos__(self):
        return TestOperation(operator.pos, self)
    def __abs__(self):
        return TestOperation(operator.abs, self)
    def __invert__(self):
        return TestOperation(operator.inv, self)

    def evaluate(self, executable, check_script, *, reporter=None):
        """
        Evaluate the score of this test structure.
        """
        if reporter is not None:
            reporter.write('')
        return 0


class TestConstant(BaseTest):
    """
    Not an actual test but a wrapper for a constant value in test struture.
    """
    def __init__(self, value):
        self.value = value

    def evaluate(self, executable, check_script, *, reporter=None):
        if reporter:
            reporter.write(self.value)
        return self.value


class TestOperation(BaseTest):
    """
    Not an actual test but a wrapper for an operation in the test structure.
    """
    def __init__(self, op, *expressions, name=None):
        self.op = op
        self.name = name if name is not None else op.__name__
        self.expressions = [
            atom if isinstance(atom, BaseTest) else TestConstant(atom)
            for atom in expressions
        ]

    def evaluate(self, executable, check_script, *, reporter=None):
        if reporter:
            reporter.write('Operation "{}"'.format(self.name))
            subreport_creator = reporter.subreport
        else:
            subreport_creator = lambda: None
        scores = [
            atom.evaluate(executable, check_script, reporter=subreport_creator())
            for atom in self.expressions
        ]
        return self.op(*scores)

    @staticmethod
    def sum(*expressions):
        """
        Special sum operator for test cases structure.
        """
        sum_op = lambda *args: sum(args)
        return TestOperation(sum_op, *expressions, name='sum')

    @staticmethod
    def max(first, *rest):
        """
        Special max operator for test cases structure.
        """
        if rest:
            return TestOperation(max, first, *rest, name='max')
        else:
            return TestOperation(max, *first, name='max')

    @staticmethod
    def min(first, *rest):
        """
        Special min operator for test cases structure.
        """
        if rest:
            return TestOperation(min, first, *rest, name='min')
        else:
            return TestOperation(min, *first, name='min')


class SimpleTest(BaseTest):
    """
    A class for simple test case, with an input file, a solution file,
    and a score limit.
    """
    def __init__(self, input_file, solution_file, score_limit, *, name=None):
        # TODO: check file exists and is absolute path
        self.input_file = input_file
        self.solution_file = solution_file
        self.score_limit = score_limit
        self.name = (name if name is not None else
                     os.path.splitext(os.path.basename(input_file))[0])

    def evaluate(self, executable, check_script, *, reporter=None):
        """
        Evaluate the score of this test case.
        """
        # TODO: implement me
        import random
        score = random.randint(0, self.score_limit)
        if reporter:
            reporter.write('{}/{} [{}] from test: {}'.format(
                score, self.score_limit, 'correct', self.name
            ))
        return score
