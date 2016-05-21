# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
import os
import os.path
from lemoneval.core.checkscript import BaseCheckScript
from lemoneval.core.executable import ExecutableFactory
from lemoneval.core.testcase import BaseTestCase


class BaseTestConfiguration(object):
    """
    Basic test configuration which does nothing.
    """
    def __init__(self, grading_dir):
        """
        Initialize the test configuration, using grading directory to keep
        final relevant files. Create the directory if not already exists.
        """
        self.grading_dir = os.path.abspath(grading_dir)
        os.makedirs(self.grading_dir, mode=0o770, exist_ok=True)
        assert(os.path.isdir(self.grading_dir))

    def pre_submit(self):
        """
        This method gets called before asking the user to submit their
        solution. Useful for generating a test case on-the-fly and give
        them to the user.
        """
        pass  # do nothing

    def post_submit(self, provided_files):
        """
        Receive solutions files submitted by the user and evaluate them.
        """
        pass  # do nothing

    def generate_report(self):
        """
        Generate a report which records the performance of a submission.
        """
        raise NotImplementedError


class SimpleTestConfiguration(BaseTestConfiguration):
    """
    A test configuration which uses a program submitted from a user to
    evaluate each test case and reports the final result.

    Attributes:
        check_script    An object of BaseCheckScript class which checks if
                        the output file is correct.
        test_structure  A tree of TestCases which contains all test cases
                        and how the final score is computed.
        score_limit     The maximum score obtained with this test structure.
        expected_files  List of files should be submitted by user.
    """
    check_script = BaseCheckScript()
    executable_factory = ExecutableFactory(require=['source_file'])
    test_structure = BaseTestCase()
    score_limit = 0

    def post_submit(self, provided_files):
        """
        Extract the submission program and run the test.
        """
        executable = self.executable_factory(provided_files)
        score, message = self.run_all_tests(executable)
        return score, message

    def run_all_tests(self, executable):
        """
        Traverse through the test structure, evaluate each test, and compute
        the final score based on the structure.
        """
        score, message = self.test_structure.evaluate(
            executable, self.check_script
        )
        return score, message
