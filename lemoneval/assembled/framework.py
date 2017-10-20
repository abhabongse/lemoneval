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

    question = parameter.TextParameter()   # question text
    answer = parameter.IntegerParameter()  # index to the right choice
    score = parameter.PositiveIntegerParameter()   # score of this question

    choice_a = parameter.TextParameter()   # choice a
    choice_b = parameter.TextParameter()   # choice b
    choice_c = parameter.TextParameter()   # choice c
    choice_d = parameter.TextParameter()   # choice d
    choice_e = parameter.TextParameter()   # choice e
    choices = [choice_a, choice_b, choice_c, choice_d, choice_e]

    def framework_validate(self):
        if not 0 <= self.answer < len(self.choices):
            raise ValueError(
                f"index for correct answer must be between 0 and "
                f"{len(self.choices)-1} but given: {self.answer!r}"
            )
