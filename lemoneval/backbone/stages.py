# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>

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
        self.__wrapped__ = setup_method

    def __call__(self, framework, session, *response_args, **response_kwargs):
        current_stage = getattr(session, "_stage_counter", 0)
        current_method = self._progress_methods[current_stage]
        stage_increment, output = current_method(
            framework, session, *response_args, **response_kwargs
        )
        session._stage_counter = current_stage + int(stage_increment)
        if session._stage_counter == len(self._progress_methods):
            raise StopIteration(output)
        self.__wrapped__ = self._progress_methods[session._stage_counter]
        return output

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return MethodType(self, instance)

    def add_stage(self, extra_method):
        """Add extra method as the next stage of `resume_session`."""
        self._progress_methods.append(extra_method)
        return self
