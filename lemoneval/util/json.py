# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>
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
    """Helper function which is called when the JSON encoder (dumper) do not
    recognize the object. This function would return the object as a dictionary
    with the following keys:

    __module__: Module string of the class of the object
    __name__: Name of the class of the object in the above module
    __args__: Necessary positional arguments (list) to the constructor of the
        class of the object upon object reconstruction.
        This is obtained by calling object.serialized_args property.
    __kwargs__: Necessary keyword-only arguments (dict) to the constructor of
        the class of the object upon object reconstruction.
        This is obtained by calling object.serialized_kwargs property.
        Special case: if said property is the string literal "__dict__" then
            then entire object.__dict__ is used.
    __dict__: Additional dictionary items to be added to object.__dict__ once
        the object is reconstructed using __args__ and __kwargs__ above.
        This is obtained by calling object.serialized_dict property.
        Special case: if said property is the string literal "__all__" then the
            entire object.__dict__ is used.
    """
    ###
    # Obtain serializable data (args, kwargs, dict)
    serializable = False
    try:
        args = obj.serialized_args; serializable = True
    except AttributeError:
        args = ()
    try:
        kwargs = obj.serialized_kwargs; serializable = True
        if kwargs == "__dict__": kwargs = obj.__dict__
    except AttributeError:
        kwargs = {}
    try:
        objdict = obj.serialized_dict; serializable = True
        if objdict == "__all__": objdict = obj.__dict__
    except AttributeError:
        objdict = {}
    if not serializable:
        raise TypeError("object not JSON serializable")
    ###
    # Prepare JSON dictionary and put all data together
    cls = type(obj)
    json_data = dict(__module__=cls.__module__, __class__=cls.__name__)
    if args:
        json_data["__args__"] = args
    if kwargs:
        json_data["__kwargs__"] = kwargs
    if objdict:
        json_data["__dict__"] = objdict
    return json_data


def _decoder_object_hook(obj):
    """Object hook helper for JSON decoder (loader) which tries to reverse the
    task of _encoder_default function.
    """
    try:
        module = importlib.import_module(obj["__module__"])
        cls = getattr(module, obj["__class__"])
        args = obj.get("__args__", ())
        kwargs = obj.get("__kwargs__", {})
        objdict = obj.get("__dict__", {})
    except:
        return obj
    else:
        obj = cls(*args, **kwargs)
        obj.__dict__.update(objdict)
        return obj


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
