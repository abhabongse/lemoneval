# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from .base import BaseExercise
from . import field


class FiveChoicesExercise(BaseExercise):
    question = field.TextField()   # question text
    answer = field.IntegerField()  # index to the right choice
    score = field.IntegerField()   # score of this question

    choice_a = field.TextField()   # choice a
    choice_b = field.TextField()   # choice b
    choice_c = field.TextField()   # choice c
    choice_d = field.TextField()   # choice d
    choice_e = field.TextField()   # choice e
    choices = [choice_a, choice_b, choice_c, choice_d, choice_e]

    def selfcheck_valid(self):
        if not 0 <= self.answer < len(self.choices):
            raise ValueError("answer was out of range")
        if not self.score > 0:
            raise ValueError("score must have been positive")
