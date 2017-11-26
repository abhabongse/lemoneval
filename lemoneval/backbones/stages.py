# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>

from functools import update_wrapper
from types import MethodType

class linear_stages(object):
    """Decorator for `framework.resume_session` to add stages to session.

    Applying this decorator to `framework.resume_session` method of a
    framework allows implementers to implement multi-stage `resume_session`
    methods as separate methods.

    See examples of usage in implementation of frameworks in `..assembled`
    package.
    """

    def __init__(self, setup_method):
        self._progress_methods = [setup_method]
        update_wrapper(self, setup_method, updated=())

    def __call__(self, framework, session, *response_args, **response_kwargs):
        current_stage = self.get_current_stage(session)
        stage_increment, output = current_stage(
            framework, session, *response_args, **response_kwargs
        )
        # Update stage counter and check if already last
        session._stage_counter += int(stage_increment)
        if session._stage_counter == len(self._progress_methods):
            raise StopIteration(output)
        return output

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return MethodType(self, instance)

    def add_stage(self, extra_method):
        """Add extra method as the next stage of `resume_session` in framework
        definition."""
        self._progress_methods.append(extra_method)
        return self

    def get_current_stage(self, session):
        """Obtain current stage method based on given session. This method
        also zero-initialize `session._stage_counter` if not already exists.
        """
        session._stage_counter = getattr(session, "_stage_counter", 0)
        current_stage = self._progress_methods[session._stage_counter]
        return current_stage


class directional_stages(object):
    """Decorator for `framework.resume_session` to add stages to session.

    Applying this decorator to `framework.resume_session` method of a
    framework allows implementers to implement multi-stage `resume_session`
    methods as separate methods.

    See examples of usage in implementation of frameworks in `..assembled`
    package.
    """
    pass
