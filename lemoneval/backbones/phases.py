# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>
"""Decorator for `framework.resume_session` to facilitate the implementation
of multi-phrase session controller. 
"""

from functools import update_wrapper, partial
from types import MethodType


class StageSequence(object):
    """Decorator for `framework.resume_session` method to implement multi-
    phase session controller in sequential stage (SS) style.

    The first decorated method will become the first stage (which is usually
    for session initialization). Subsequent stages are added to the sequence
    by decorating them with `resume_session.add_stage`. For example::

        class C(framework.BaseFramework):
            [...]

            def check_correct(self, session, input_data):
                [...]

            @phases.StagesSequence
            def resume_session(self, session):
                [...]
                return True, output_data

            @resume_session.add_stage
            def _check_stage(self, session, input_data):
                # Method _second_stage is meant to be ignored
                if self.check_correct(session, input_data):
                    return True, "correct"
                return False, "try again"

    All stage methods must accept the framework (`self` in the above method)
    and `session` objects as the first two positional arguments. The remaining
    arguments could be any stage-specific configuration (such as `input_data`
    in `_check_stage` method above).

    All stage methods must return a 2-tuple, the first element in which is a
    boolean indicating whether the session is allowed to move on from the
    current stage to the next stage; the second element is the response to
    given to the session player.

    There are 2 ways to terminate the session:

        1. The final stage method returns the tuple `(True, summary)`, where
            the `summary` encapsulates the end result of the session.

        2. Any stage methods (prematurely) raises `StopIteration(summary)`,
            where the `summary` is the same as above.

    See real examples of usage in implementation of pre-assembled
    frameworks in `..assembled` package.

    Note:
        This class uses `session._stage_counter` to keep track of which stage
        is current.
    """

    def __init__(self, setup_method):
        self._methods = [setup_method]
        update_wrapper(self, setup_method, updated=())

    def __call__(self, framework, session, *args, **kwargs):
        stage_method = self.get_current_phase(session)
        stage_increment, result = stage_method(
            framework, session, *args, **kwargs
        )
        # Increment stage counter according and check if already at the end
        # Note: session._stage_counter is guaranteed to exists by calling
        # `self.get_current_phase` as seen above.
        session._stage_counter += int(bool(stage_increment))
        if session._stage_counter == len(self._methods):
            raise StopIteration(result)
        return result

    def __get__(self, framework, owner):
        if framework is None:
            return self
        return MethodType(self, framework)

    def add_stage(self, extra_method):
        """Add extra method as the next stage of `resume_session` in framework
        definition.
        """
        self._methods.append(extra_method)
        return self

    def get_current_phase(self, session):
        """Obtain current stage method based on given session. This method
        also zero-initialize `session._stage_counter` if not already exists.
        """
        session._stage_counter = getattr(session, "_stage_counter", 0)
        try:
            stage_method = self._methods[session._stage_counter]
        except IndexError as e:
            if session._stage_counter == len(self._methods):
                raise AttributeError("no more callable stages") from e
            raise
        return stage_method


class StateMachine(object):
    """Decorator for `framework.resume_session` method to implement multi-
    phase session controller in finite state machine (FSM) style. However,
    note that this is strictly not a state machine as defined in Models of
    Computation courses.

    The first decorated method will become the starting state (which is usually
    for session initialization). Other states are added to the network by
    decorating them with `resume_session.add_state`. Ending states are implicit
    and does not require an extra method.

    All non-starting-or-ending states requires a label (which must be a
    valid python variable name). The starting state and the ending state have
    the special pseudo-label '$start' and '$end' respectively. In the context
    of each state, '$self' refers to its own state. Additionally, every state
    are also 0-indexed in the order of their addition into the system.

    For example::

        class C(framework.BaseFramework):
            [...]

            def check_correct(self, session, input_data):
                [...]

            @phases.StateMachine
            def resume_session(self, session):
                # Label: '$start' or 0
                [...]
                return "check_answer", output_data

            @resume_session.add_state(label="check_answer")
            def _check_answer_state(self, session, input_data):
                # Label: 'check_answer' or 1
                # Name _check_answer_state is meant to be ignored
                if self.check_correct(session, input_data):
                    return "$end", "correct"
                return "$self", "try again"

    All stage methods must accept the framework (`self` in the above method)
    and `session` objects as the first two positional arguments. The remaining
    arguments could be any stage-specific configuration (such as `input_data`
    in `_check_answer_state` method above).

    All stage methods must return a 2-tuple, the first element in which is a
    string indicating the next state to whcih the session is allowed to move on
    from the current state; the second element is the response to given to the
    session player.

    There are 2 ways to terminate the session:

        1. Any state method returns the tuple `("$end", summary)`, where
            the `summary` encapsulates the end result of the session.

        2. Any stage methods (prematurely) raises `StopIteration(summary)`,
            where the `summary` is the same as above.

    See real examples of usage in implementation of pre-assembled
    frameworks in `..assembled` package.

    Note:
        This class uses `session._state_label` to keep track of which stage
        is current.
    """

    def __init__(self, setup_method):
        self._methods = { '$start': setup_method, 0: setup_method }
        self._methods_count = 1
        update_wrapper(self, setup_method, updated=())

    def __call__(self, framework, session, *args, **kwargs):
        state_method = self.get_current_phase(session)
        session._state_label, result = state_method(
            framework, session, *args, **kwargs
        )
        # Update state counter according and check if already at the end
        # Note: session._state_label is guaranteed to exists by calling
        # `self.get_current_phase` as seen above.
        if session._state_label == "$end":
            raise StopIteration(result)
        if session._state_label not in self._methods:
            raise ValueError("next state not valid")
        return result

    def __get__(self, framework, owner):
        if framework is None:
            return self
        return MethodType(self, framework)

    def add_state(self, extra_method=None, *, label):
        """Add extra method as the next state of `resume_session` in framework
        definition.
        """
        if extra_method is None:
            return partial(self.add_state, label=label)
        self._methods[label] = extra_method
        self._methods[self._methods_count] = extra_method
        self._methods_count += 1
        return self

    def get_current_phase(self, session):
        """Obtain current state method based on given session. This method
        also zero-initialize `session._state_label` if not already exists.
        """
        session._state_label = getattr(session, "_state_label", "$start")
        try:
            state_method = self._methods[session._state_label]
        except KeyError as e:
            if session._state_label == "$end":
                raise AttributeError("no more callable state") from e
            raise
        return state_method
