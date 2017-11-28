# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>

from ...backbones import frameworks, parameters
from ...backbones.phases import StateMachine

class AddingNumbersFramework(frameworks.BaseFramework):
    """Simple algebra question: adding two integers which are uniformly
    randomized from within the given bound.

    parameters:
        lower_bound: Lower bound of randomized integers
        upper_bound: Upper bound of randomized integers
        score: Positive value score
    """
    lower_bound = parameters.Parameter(dtype=int)
    upper_bound = parameters.Parameter(dtype=int)
    score = parameters.Parameter(dtype=int)

    @score.add_validators  # score must be positive
    def positive_score(score):
        if score > 0:
            return True
        raise ValueError("'score' should be positive")

    def framework_validate(self):
        # Lower bound must be no greater than upper bound
        if self.lower_bound > self.upper_bound:
            raise ValueError(
                f"Lower bound should not be greater than upper bound but "
                f"{self.lower_bound} and {self.upper_bound} are given resp."
            )

    @StateMachine  # generate numbers
    def resume_session(self, session):
        import random
        session.a = random.randint(self.lower_bound, self.upper_bound)
        session.b = random.randint(self.lower_bound, self.upper_bound)
        return "check_answer", { "a": session.a, "b": session.b }

    @resume_session.add_state(label="check_answer")  # check answer
    def _check_answer(self, session, *, response_sum):
        is_correct = (response_sum == session.a + session.b)
        return "$end", {
            "status": "correct" if is_correct else "incorrect",
            "score": is_correct * self.score
        }
