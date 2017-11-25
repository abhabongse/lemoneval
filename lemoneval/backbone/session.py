# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>
"""A session object defines an interaction of a player with a particular
exercise framework. A session could be created in one of two ways:

    1. A new session is created by calling `framework.create_session` from a
        framework object.

    2. The session can be restored from JSON serialization by using `load[s]``
        functions defined in `..util.json`.

Interactions with session objects depends on different types of frameworks
and is described by the method `framework.progress_session`.
"""

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
        `_prepared_kwargs`) to the method `framework.progress_session` to
        resume the session.
        """
        if self.has_finished:
            raise StopIteration(self._summary)
        try:
            self._public = self._framework.progress_session(
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
        # Responses to be delivered to `framework.progress_session`
        self._prepared_args = ()
        self._prepared_kwargs = {}

    def prepare(self, *response_args, **response_kwargs):
        """Calling this method followed by `__next__` method is equivalent to
        calling `submit` method directly. This helps working with iterables
        easier such as for loops.
        """
        self._prepared_args = response_args
        self._prepared_kwargs = response_kwargs

    def submit(self, *response_args, **response_kwargs):
        """Attempts to make progress on the session by submitting responses.

        This method is the gateway to `framework.progress_session`. The first
        call to this is expected to initialize the session with empty response.
        Every call to this method either returns new public data or raises a
        `StopIteration` with final summary.
        """
        self._prepared_args = response_args
        self._prepared_kwargs = response_kwargs
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

    def to_json(self, fp=None, no_return=False):
        """Serialize the session into JSON string (and additionally write to
        a file if file pointer `fp` is provided)."""
        if fp is not None:
            from ..util.json import dump as write_json_file
            write_json_file(self, fp)
        if not no_return:
            from ..util.json import dumps as get_json_str
            return get_json_str(self)
