# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>

from ...backbone import framework, parameter
from ...backbone.stages import linear_stages

class MultipleChoicesFramework(framework.BaseFramework):
    """Multiple choice question framework with one correct answer.

    parameters:
        question: Question text
        choices: Sequence of choices texts
        answer: 0-index of the correct answer in choices
        score: Positive value score
    """
    question = parameter.Parameter(dtype=str)  # question text
    choices = parameter.SequenceParameter(dtype=str)   # choices
    answer = parameter.Parameter(dtype=int)    # index to the right choice
    score = parameter.Parameter(dtype=int)     # score of this question

    @score.add_validators  # score must be positive
    def positive_score(score):
        if score > 0:
            return True
        raise ValueError("'score' should be positive")

    def framework_validate(self):
        # Answer index must be within bounds
        if not 0 <= self.answer < len(self.choices):
            raise ValueError(
                f"the index for correct answer must be between 0 and "
                f"{len(self.choices)-1} but {self.answer!r} was given"
            )

    @linear_stages  # show question
    def resume_session(self, session):
        return True, {
            "question": self.question,
            "choices": self.choices
        }

    @resume_session.add_stage  # check answer
    def resume_session(self, session, *, selected_choice):
        session.selected_choice = selected_choice
        is_correct = (session.selected_choice == self.answer)
        return True, {
            "status": "correct" if is_correct else "incorrect",
            "score": is_correct * self.score
        }


class FiveChoicesFramework(MultipleChoicesFramework):
    """Multiple choice question framework with 5 choices."""

    choices = parameter.SequenceParameter(dtype=str, length=5)
