# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>

from ...backbones import frameworks, parameters
from ...backbones.stages import StagesSequence

class MultipleChoicesFramework(frameworks.BaseFramework):
    """Multiple choice question framework with one correct answer.

    parameters:
        question: Question text
        choices: Sequence of choices texts
        answer: 0-index of the correct answer in choices
        score: Positive value score
    """
    question = parameters.Parameter(dtype=str)  # question text
    choices = parameters.SequenceParameter(dtype=str)   # choices
    answer = parameters.Parameter(dtype=int)    # index to the right choice
    score = parameters.Parameter(dtype=int)     # score of this question

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

    @StagesSequence  # show question
    def resume_session(self, session):
        """Initiate the exercise interaction."""
        return True, {
            "question": self.question,
            "choices": self.choices
        }

    @resume_session.add_stage  # check answer
    def _check_answer(self, session, *, selected_choice):
        """Check the answer."""
        session.selected_choice = selected_choice
        is_correct = (session.selected_choice == self.answer)
        return True, {
            "status": "correct" if is_correct else "incorrect",
            "score": is_correct * self.score
        }


class FiveChoicesFramework(MultipleChoicesFramework):
    """Multiple choice question framework with 5 choices."""

    choices = parameters.SequenceParameter(dtype=str, length=5)
