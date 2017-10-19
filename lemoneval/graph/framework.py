# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from .base import BaseFramework
from . import field


class FiveChoicesFramework(BaseFramework):
    """Multiple choice question framework with 1 correct answer out of 5.

    Fields:
        question: Question text
        answer: The 0-index of the correct answer
        score: Positive value score
        choice_a, choice_b, choice_c, choice_d, choice_e:
            Choice text for each of the 5 choices.
    """

    question = field.TextField()   # question text
    answer = field.IntegerField()  # index to the right choice
    score = field.IntegerField()   # score of this question

    choice_a = field.TextField()   # choice a
    choice_b = field.TextField()   # choice b
    choice_c = field.TextField()   # choice c
    choice_d = field.TextField()   # choice d
    choice_e = field.TextField()   # choice e
    choices = [choice_a, choice_b, choice_c, choice_d, choice_e]

    def framework_validate(self):
        if not 0 <= self.answer < len(self.choices):
            raise ValueError(
                f"index for correct answer must be between 0 and "
                f"{len(self.choices)-1} but given: {self.answer!r}"
            )
        if not self.score > 0:
            raise ValueError(
                f"expecting a positive score but given: {self.score!r}"
            )
