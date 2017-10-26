# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from ..backbone import framework, parameter

class FiveChoicesFramework(framework.BaseFramework):
    """Multiple choice question framework with 1 correct answer out of 5.

    parameters:
        question: Question text
        answer: The 0-index of the correct answer
        score: Positive value score
        choice_a, choice_b, choice_c, choice_d, choice_e:
            Choice text for each of the 5 choices.
    """

    question = parameter.Parameter(dtype=str)  # question text
    choices = parameter.SequenceParameter(dtype=str, length=5)   # choices
    answer = parameter.Parameter(dtype=int)    # index to the right choice
    score = parameter.Parameter(dtype=int)     # score of this question
    score.add_validators(lambda x: x > 0)

    def framework_validate(self):
        if not 0 <= self.answer < len(self.choices):
            raise ValueError(
                f"the index for correct answer must be between 0 and "
                f"{len(self.choices)-1} but {self.answer!r} was given"
            )
