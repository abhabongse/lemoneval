# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>

from ...backbone import framework, parameter

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

    def progress_session(self, session, *, choose=None):
        # 1: Session launched for the first time
        if not hasattr(session, "stage"):
            session.stage = 0
            return dict(question=self.question, choices=self.choices)
        # 2: A response is given to the session, and STOP!
        if session.stage == 0:
            session.stage = 1
            session.chosen = choose
            is_correct = (session.chosen == self.answer)
            raise StopIteration ({
                "status": "correct" if is_correct else "incorrect",
                "score": is_correct * self.score
            })

class FiveChoicesFramework(MultipleChoicesFramework):
    """Multiple choice question framework with 5 choices."""

    choices = parameter.SequenceParameter(dtype=str, length=5)
