# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from ...backbone import framework, parameter

class AddingNumbersFramework(framework.BaseFramework):
    """Simple algebra question: adding two integers which are uniformly
    randomized from within the given bound.

    parameters:
        lower_bound: Lower bound of randomized integers
        upper_bound: Upper bound of randomized integers
        score: Positive value score
    """
    lower_bound = parameter.Parameter(dtype=int)
    upper_bound = parameter.Parameter(dtype=int)
    score = parameter.Parameter(dtype=int)

    def framework_validate(self):
        # Lower bound must be no greater than upper bound
        if self.lower_bound > self.upper_bound:
            raise ValueError(
                f"Lower bound should not be greater than upper bound but "
                f"{self.lower_bound} and {self.upper_bound} are given resp."
            )

    def progress_session(self, session, response):
        # 1: Session launched for the first time
        if not hasattr(session, "stage"):
            session.stage = 0
            return self.randomize_numbers(session)
        # 2: A response is given to the session, and STOP!
        if session.stage == 0:
            session.stage = 1
            summary = self.check_response(session, response)
            raise StopIteration(summary)

    def randomize_numbers(self, session):
        import random
        session.a = random.randint(self.lower_bound, self.upper_bound)
        session.b = random.randint(self.lower_bound, self.upper_bound)
        return dict(a=session.a, b=session.b)

    def check_response(self, session, answered_sum):
        is_correct = (answered_sum == session.a + session.b)
        return {
            "status": "correct" if is_correct else "incorrect",
            "score": is_correct * self.score
        }
