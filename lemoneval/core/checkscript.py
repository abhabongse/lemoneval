# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
import decimal
import filecmp
import os.path
import subprocess


class BaseCheckScript(object):
    """
    A check script class which compares two files (output and solution)
    byte-by-byte.
    """
    def evaluate(self, input_file, output_file, solution_file, score_limit):
        """
        Given an input file, an output file, and a solution file, compare the
        output and the solution files to see if they are exactly the same.
        It returns a tuple of resulting score and a message.
        """
        if self.check_answer(input_file, output_file, solution_file):
            return score_limit, 'Correct'
        else:
            return 0, 'Incorrect'

    def check_answer(self, input_file, output_file, solution_file):
        """
        Compare the output and the solution files.
        """
        filecmp.clear_cache()
        return filecmp.cmp(output_file, solution_file, shallow=False)


class StandardCheckScript(BaseCheckScript):
    """
    A check script class which compares two files (output and solution)
    word-by-word. Words in each lines must be exactly the same, with one or
    more blank spaces separating each word in the same line.
    """
    def check_answer(self, input_file, output_file, solution_file):
        """
        Compare the output and the solution files to see if they are
        word-by-word the same. It returns a tuple of resulting score and
        a message.
        """
        def words_stream(fileobj):
            """
            Return an iterable of words from a given file object, with a
            new line character as its own word.
            """
            for line in fileobj:
                for word in line.split():
                    yield word
                yield '\n'

        with open(output_file) as fout, open(solution_file) as fsol:
            stream_a = words_stream(fout); stream_b = words_stream(fsol)
            if any(word_a != word_b
                   for (word_a, word_b) in zip(stream_a, stream_b)):
                return False
            try:
                next(stream_a)
            except StopIteration:
                pass
            else:
                return False
            try:
                next(stream_b)
            except StopIteration:
                pass
            else:
                return False
        return True


class FileCheckScript(BaseCheckScript):
    """
    A check script class which utilizes an external check script executable
    to check if the output file is correct given the input file and the
    solution file. The prorgram should output two lines: the first being the
    assigned score, and the second being the message.
    """
    def __init__(self, check_script):
        """
        Initialize the file check script.
        """
        self.check_script = os.path.abspath(check_script)

    def evaluate(self, input_file, output_file, solution_file, score_limit):
        """
        Given an input file, an output file, and a solution file, compare the
        output and the solution files using the check script.
        """
        result = subprocess.run(
            [self.check_script, input_file.path, output_file.path,
             solution_file.path, score_limit], stdout=subprocess.PIPE
        )
        stdout_lines = result.stdout.split('\n')
        return decimal.Decimal(stdout_lines[0]), stdout_lines[1]
