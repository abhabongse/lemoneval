# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>

class Session(object):
    """Session object representing a player interacting with a particular
    exercise framework.
    """
    def __init__(self, framework):
        self._framework = framework
        self._prepared = None  # prepared response when next() is called

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

    @property
    def serialized_args(self):
        return (self._framework,)

    @property
    def serialized_dict(self):
        copied_dict = self.__dict__.copy()  # type: dict
        copied_dict.pop("_framework")
        return copied_dict

    def __iter__(self):
        return self

    def __next__(self):
        return self.submit(self._prepared)

    def prepare(self, response):
        """Calling this method followed by __next__ method is an equivalent
        of calling submit method directly. This helps working with iterables
        easier such as in for loop.
        """
        self._prepared = response

    def submit(self, response):
        """Send a response (dict) to the session. This method is an analog of
        coroutine's send() method.
        """
        if self.has_finished:
            raise StopIteration(self._summary)
        self._prepared = None
        try:
            self._public = self._framework.progress_session(self, response)
            return self._public
        except StopIteration as e:
            self._public = e.value
            self._summary = e.value
            raise

    @property
    def has_started(self):
        """Boolean indicating whether the session has started with at least
        one iteration (at least a call to next/submit).
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
        raise AttributeError("session not yet started") from e

    @property
    def summary_data(self):
        """Public data of the session at the current time. Available after the
        first iteration of the session (otherwise AttributeError is raised).
        """
        if self.has_finished:
            return self._summary
        raise AttributeError("session not yet finished") from e

    def to_json(self):
        """Serialize the session into JSON string."""
        from ..util.json import to_json as _to_json
        return _to_json(self)

    @staticmethod
    def from_json(s):
        """Deserialize the session from JSON string."""
        from ..util.json import from_json as _from_json
        return _from_json(s)
