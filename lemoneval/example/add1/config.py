# An example of a test configuration file of a problem.
# Author: Abhabongse Janthong <abhabongse@gmail.com>
import os.path
from lemoneval.core.checkscript import StandardCheckScript
from lemoneval.core.testconfig import SimpleTestConfiguration
from lemoneval.core.testcase import SimpleTestCase, TestCaseOperation

# Obtain the directory in which this source file is located.
this_dir = os.path.dirname(os.path.abspath(__file__))
test_cases = [
    SimpleTestCase(
        os.path.join(this_dir, '{}.in'.format(t)),
        os.path.join(this_dir, '{}.sol'.format(t)),
        10
    ) for t in range(1, 5)
]

# Defualt test configuration
class DefaultTestConfiguration(SimpleTestConfiguration):
    check_script = StandardCheckScript()
    test_structure = TestCaseOperation.sum(
        TestCaseOperation.min(test_cases[0], test_cases[1]),
        TestCaseOperation.min(test_cases[2], test_cases[3]),
        20
    )
    score_limit = 40
