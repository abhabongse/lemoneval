# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from ..backbone import framework, parameter

class FiveChoicesFramework(framework.BaseFramework):
    """Multiple choice question framework with 1 correct answer out of 5.

    parameters:
        question: Question text
        choices: List of 5 choice texts
        answer: The 0-index of the correct answer
        score: Positive value score
    """

    question = parameter.Parameter(dtype=str)  # question text
    choices = parameter.SequenceParameter(dtype=str, length=5)   # choices
    answer = parameter.Parameter(dtype=int)    # index to the right choice
    score = parameter.Parameter(dtype=int)     # score of this question
    @score.add_validators
    def positive_score(score):
        if score <= 0:
            raise ValueError("'score' should be positive")
        return True

    def _framework_validate(self):
        if not 0 <= self.answer < len(self.choices):
            raise ValueError(
                f"the index for correct answer must be between 0 and "
                f"{len(self.choices)-1} but {self.answer!r} was given"
            )
