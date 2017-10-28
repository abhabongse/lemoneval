# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
"""This module provides two functions: to_json and from_json. They work
together to serialize and deserialize objects of custom classes.

When an object is serialized, the property object.serializable_to_json will be
invoked. It should return a tuple of positional and keyword arguments needed
to reconstruct the object with __init__ method. Alternatively, it could just
be the string literal "__dict__" so that the entire object.__dict__ would be
used as keyword arguments dictionary.
"""

import importlib
import json


def _encoder_default(obj):
    try:
        pkargs = obj.serializable_to_json
    except AttributeError as e:
        raise TypeError("object not JSON serializable") from e
    try:
        if pkargs == "__dict__":
            args = ()
            kwargs = obj.__dict__
        else:
            args, kwargs = pkargs
            if not isinstance(args, list) or not isinstance(kwargs, dict):
                raise TypeError
    except TypeError as e:
        raise TypeError(
            "serializable_to_json must be either a tuple of (positional "
            "arguments list, keyword-only arguments dict) or the string "
            "literal '__dict__'"
        ) from e
    cls = type(obj)
    json_dict = dict(__module__=cls.__module__, __class__=cls.__name__)
    if args:
        json_dict["__args__"] = args
    if kwargs:
        json_dict["__kwargs__"] = kwargs
    return json_dict


def _decoder_object_hook(obj):
    try:
        module = importlib.import_module(obj["__module__"])
        cls = getattr(module, obj["__class__"])
        args = obj.get("__args__", ())
        kwargs = obj.get("__kwargs__", {})
    except:
        return obj
    else:
        return cls(*args, **kwargs)


def to_json(o):
    """Serialize object into JSON string."""
    return json.dumps(o, indent=2, default=_encoder_default)

def to_json_file(o, fp):
    """Serialize object into JSON file."""
    return json.dump(o, fp, indent=2, default=_encoder_default)


def from_json(s):
    """Return python object from JSON string."""
    return json.loads(s, object_hook=_decoder_object_hook)

def from_json_file(fp):
    """Return python object from JSON string."""
    return json.load(fp, object_hook=_decoder_object_hook)
