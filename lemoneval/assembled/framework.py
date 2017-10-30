# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from ..backbone import framework, parameter, session

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

    def progress_session(self, session, response):
        # 1: Session launched for the first time
        if not hasattr(session, "stage"):
            session.stage = 0
            return dict(question=self.question, choices=self.choices)
        # 2: A response is given to the session, and STOP!
        if session.stage == 0:
            session.stage = 1
            session.choose = response.get("choose", None)
            is_correct = (session.choose == self.answer)
            session.report = {
                "status": "correct" if is_correct else "incorrect",
                "score": is_correct * self.score
            }
        raise StopIteration



class FiveChoicesFramework(MultipleChoicesFramework):
    """Multiple choice question framework with 5 choices."""

    choices = parameter.SequenceParameter(dtype=str, length=5)
