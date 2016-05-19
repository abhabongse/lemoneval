# An example of a test configuration file of a problem.
# Author: Abhabongse Janthong <abhabongse@gmail.com>
import os.path
from lemoneval.core.checkscript import StandardCheckScript
from lemoneval.core.testconfig import SimpleTestConfiguration
from lemoneval.core.testcase import SimpleTestCase

# Obtain the directory in which this source file is located.
this_dir = os.path.dirname(os.path.abspath(__file__))

# Defualt test configuration
class DefaultTestConfiguration(SimpleTestConfiguration):
    check_script = StandardCheckScript()
    test_structure = sum(
        SimpleTestCase(
            os.path.join(this_dir, '{}.in'.format(t)),
            os.path.join(this_dir, '{}.sol'.format(t)),
            10 * t
        )
        for t in range(1, 5)
    )
    score_limit = 100
