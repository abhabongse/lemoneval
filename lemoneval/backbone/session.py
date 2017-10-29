# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

class Session(object):
    """Session object representing a player interacting with a particular
    exercise framework.
    """
    def __init__(self, framework):
        self._framework = framework

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
        return self.submit({})

    def submit(self, response):
        """Send a response (dict) to the session. This method is an analog of
        generator's send() method.
        """
        try:
            self._public = self._framework.progress_session(self, response)
            return self._public
        except StopIteration:
            self._public = self.report
            raise

    def fetch(self):
        """Return public data which is avaliable after the first iteration."""
        return getattr(self, "_public", None)

    def to_json(self):
        """Serialize the session into JSON string."""
        from ..util.json import to_json as _to_json
        return _to_json(self)

    @staticmethod
    def from_json(s):
        """Deserialize the session from JSON string."""
        from ..util.json import from_json as _from_json
        return _from_json(s)
