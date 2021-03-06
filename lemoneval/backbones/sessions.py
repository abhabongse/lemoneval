# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>
"""A session object defines an interaction of a player with a particular
exercise framework. A session could be created in one of two ways:

    1. A new session is created by calling `framework.create_session` from a
        framework object.

    2. The session can be restored from JSON serialization by using `load[s]``
        functions defined in `..util.json`.

Interactions with session objects depends on different types of frameworks
and is described by the method `framework.resume_session`.
"""

from functools import partial, update_wrapper, WRAPPER_ASSIGNMENTS
from types import MethodType
from ..utils.decorators import CallableWrapper
from ..utils.docstrings import trim


class _resumable_method(CallableWrapper):
    """Every time `session.wrapped` method binding occurs, update
    documentation attributes on the method.
    """
    def bind_hook(self, session, session_cls):
        resume_func = session._framework.resume_session
        if hasattr(resume_func, "get_current_phase"):
            resume_func = resume_func.get_current_phase(session)
        resume_method = MethodType(resume_func, session)
        update_wrapper(self, resume_method, updated=())
        self.__doc__ = f"{trim(self.__doc__)}\n\n{trim(self._func.__doc__)}"


class Session(object):
    """Defines an interaction of a player with an exercise framework.

    A session object are not meant to be constructed directly. Use the method
    `framework.create_session` to initiate a new session from a a frameworks
    instance object.
    """

    def __init__(self, framework):
        self._framework = framework
        self._clear_prepared()  # initialize prepared response attributes

    def __repr__(self):
        formatted_dict_items = (
            (name, repr(value).replace("\n", "\n  "))
            for name, value in self.__dict__.items()
        )
        formatted_dict_text = ",\n".join(
            f"  {name}={value}"
            for name, value in formatted_dict_items
        )
        return f"{type(self).__qualname__}(\n{formatted_dict_text}\n)"

    def __iter__(self):
        return self

    def __next__(self):
        return self._resume()

    @property
    def serialized_args(self):
        return (self._framework,)

    @property
    def serialized_dict(self):
        copied_dict = self.__dict__.copy()  # type: dict
        copied_dict.pop("_framework")
        return copied_dict

    def _resume(self):
        """Obtain and pass along prepared responses (`_prepared_args` and
        `_prepared_kwargs`) to the method `framework.resume_session` to
        resume the session.
        """
        if self.has_finished:
            raise StopIteration(self._summary)
        try:
            self._public = self._framework.resume_session(
                self, *self._prepared_args, **self._prepared_kwargs
            )
            return self._public
        except StopIteration as e:
            self._public = e.value
            self._summary = e.value
            raise
        finally:
            self._clear_prepared()  # reset prepared responses

    def _clear_prepared(self):
        """Clear prepared responses."""
        # Responses to be delivered to `framework.resume_session`
        self._prepared_args = ()
        self._prepared_kwargs = {}

    @_resumable_method
    def prepare(self, *args, **kwargs):
        """Calling this method followed by `__next__` method is equivalent to
        calling `submit` method directly. This helps working with iterables
        easier such as for loops.
        """
        self._prepared_args = args
        self._prepared_kwargs = kwargs

    @_resumable_method
    def submit(self, *args, **kwargs):
        """Attempts to make progress on the session by submitting responses.

        This method is the gateway to `framework.resume_session`. The first
        call to this is expected to initialize the session with empty response.
        Every call to this method either returns new public data or raises a
        `StopIteration` with final summary.
        """
        self._prepared_args = args
        self._prepared_kwargs = kwargs
        return self._resume()

    @property
    def has_started(self):
        """Boolean indicating whether the session has started with at least
        one iteration (i.e. at least one call to `__next__` or `submit`).
        """
        return hasattr(self, "_public")

    @property
    def has_finished(self):
        """Boolean indicating whether the session has ended."""
        return hasattr(self, "_summary")

    @property
    def public_data(self):
        """Public data of the session at the current time. Available after the
        first iteration of the session (otherwise AttributeError is raised).
        """
        if self.has_started:
            return self._public
        raise AttributeError("session not yet started")

    @property
    def summary_data(self):
        """Public data of the session at the current time. Available after the
        last iteration of the session (otherwise AttributeError is raised).
        """
        if self.has_finished:
            return self._summary
        raise AttributeError("session not yet finished")

    def to_json(self, fp=None, string_return=True):
        """Serialize the session into JSON string (and additionally write to
        a file if file pointer `fp` is provided)."""
        if fp is not None:
            from ..utils.json import dump as write_json_file
            write_json_file(self, fp)
        if string_return:
            from ..utils.json import dumps as get_json_str
            return get_json_str(self)
