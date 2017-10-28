# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

class Session(object):
    """Session object representing a player interacting with a particular
    exercise framework.
    """
    serializable_to_json = "__dict__"

    def __init__(self, framework, stage=0):
        self.framework = framework
        self.stage = stage

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

    def to_json(self):
        from ..util.json import to_json as _to_json
        return _to_json(self)

    @classmethod
    def from_json(cls, s):
        from ..util.json import from_json as _from_json
        return _from_json(s)
