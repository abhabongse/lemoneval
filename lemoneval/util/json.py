# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
"""This module provides two functions: to_json and from_json. They work
together to serialize and deserialize objects of custom classes.

When an object is serialized, the property object.serializable_to_json will be
invoked. It should return the JSON serializable python data that would be
needed as argument of __init__ in order to reconstruct the object. It could
also be an Ellipsis (...) to indicate that object.__dict__ is to be used for
JSON serialization.
"""

import importlib
import json


def to_json(o):
    """Serialize object into JSON string."""
    import json
    def _default(obj):
        if not hasattr(obj, "serializable_to_json"):
            raise TypeError("object not JSON serializable")
        args = obj.serializable_to_json
        if args is Ellipsis:
            args = obj.__dict__
        cls = type(obj)
        clsname = cls.__name__
        clsmodule = cls.__module__
        return dict(__module__=clsmodule, __class__=clsname, __args__=args)
    return json.dumps(o, indent=2, default=_default)


def from_json(s):
    """Return python object from JSON string."""
    import importlib
    import json
    def _object_hook(obj):
        try:
            module = importlib.import_module(obj["__module__"])
            cls = getattr(module, obj["__class__"])
            args = obj["__args__"]
        except:
            return obj
        else:
            if isinstance(args, dict):
                return cls(**args)
            elif isinstance(args, list):
                return cls(*args)
            else:
                return cls(args)
    return json.loads(s, object_hook=_object_hook)
