# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>
"""JSON serialization and deserialization for custom classes.

This module provides four functions: `dumps`, `dump`, `loads`, and `load`,
which behaves mostly the same as their counterparts in `json` built-in package
but with customized serialization.

Custom classes are expected to implement **at least one** the following
attributes, either as a constant or a property onto class method:

    object.serialized_args: This attribute should result in a list of values
        which can be supplied to the class constructor via positional
        arguments to reconstruct the object.

        This works in conjucntion with named keyword arguments obtained via
        `object.serialized_kwargs` during the object construction.

    object.serialized_kwargs: This attribute should result in a dictionary of
        key-value pairs which can be supplied to the class constructor via
        named keyword arguments to reconstruct the object.

        This works in conjunction with positional arguments obtained via
        `object.serialized_args` during the object construction.

        Alternatively, if this attribute results in a string `__dict__` then
        it is as if `object.__dict__` is returned.

    object.serialized_dict: This attribute should result in a dictionary of
        key-value pairs which will be used to **update** `object.__dict__`
        attribute after the object has already been reconstructed via the above
        two attributes.

        Alternatively, if this attribute results in a string `__all__` then
        it is as if `object.__dict__` is returned.

The structure of JSON upon object serialization is a dictionary with the
following key-value pairs:

    __module__: Module string of the object class.
    __class__: Name of the object class as defined in `__module__`
    __args__: Mandatory positional arguments (list) to be supplemented upon
        object instance reconstruction by class constructor.
    __kwargs__: Mandatory named keyword arguments (dict) to be supplemented
        upon object reconstruction by class constructor.
    __dict__: Additional dictionary items to be added to `object.__dict__`
        once the object is reconstructed by constructor.
"""

from functools import partial
import importlib
import json


def _encoder_default(o):
    """Helper function called by JSON encoder when it does not recognize the
    object of custom classes.

    This function is typically supplied as `default` argument to the JSON
    encoder. It utilizes three attributes: `object.serialized_args`,
    `object.serialized_kwargs`, and `object.serialized_dict` to provide a
    JSON-compatible object serialization for custom classes.

    More details are outlined in module-level docstring.
    """
    # Obtain serializable data: __args__, __kwargs__, __dict__
    serializable = False
    try:
        s_args = o.serialized_args; serializable = True
    except AttributeError:
        s_args = ()
    try:
        s_kwargs = o.serialized_kwargs; serializable = True
    except AttributeError:
        s_kwargs = {}
    else:
        if s_kwargs == "__dict__": s_kwargs = o.__dict__
    try:
        s_dict = o.serialized_dict; serializable = True
    except AttributeError:
        s_dict = {}
    else:
        if s_dict == "__all__": s_dict = o.__dict__

    # Check if object is not customized for JSON serialization
    if not serializable:
        raise TypeError("object not JSON serializable")

    # Check whether the class is defined at top-level of the module
    cls = type(o)
    if cls.__name__ != cls.__qualname__:
        raise TypeError("object class not defined at top-level")

    # Initialize JSON data with module and class names, and populate
    # other serialized attribute as needed.
    data = dict(__module__=cls.__module__, __class__=cls.__name__)
    if s_args:
        data["__args__"] = s_args
    if s_kwargs:
        data["__kwargs__"] = s_kwargs
    if s_dict:
        data["__dict__"] = s_dict
    return data


def _decoder_object_hook(data):
    """Helper function called by JSON decoder to reverse `_encoder_default`.

    This function is typically supplied as `object_hook` argument to JSON
    decoder in order to reconstruct the object instance of customized classes.

    More details are outlined in module-level docstring.
    """
    try:
        module = importlib.import_module(data["__module__"])
        cls = getattr(module, data["__class__"])
        s_args = data.get("__args__", ())
        s_kwargs = data.get("__kwargs__", {})
        s_dict = data.get("__dict__", {})
    except:
        return data
    else:
        o = cls(*s_args, **s_kwargs)
        o.__dict__.update(s_dict)
        return o


# Define customized versions of dump[s] and load[s] functions
dumps = partial(json.dumps, indent=2, default=_encoder_default)
dump = partial(json.dump, indent=2, default=_encoder_default)
loads = partial(json.loads, object_hook=_decoder_object_hook)
load = partial(json.load, object_hook=_decoder_object_hook)
