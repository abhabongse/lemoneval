# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>
"""Decorator helpers."""

from functools import update_wrapper
from types import MethodType


class CallableWrapper(object):
    """Decorator which allows injection into decorated object method.

    This class takes in an object method (a function) and wraps it inside a
    new callable proxy method. There are 2 hooks being called in this class.

        1. `init_hook`: Method which gets called when the proxy method
            (function) is initialized with `__init__`.

        2. `bind_hook`: Method which gets called when the proxy method
            (function) is binded to an instance object.

    One usage of `bind_hook` of this class is to call update the callable
    proxy method with `functools.update_wrapper` to provide a more accurate
    docstrings, signatures, etc.
    """

    def __init__(self, func):
        self._func = func
        self.init_hook()

    def init_hook(self):
        update_wrapper(self, self._func, updated=())

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        self.bind_hook(instance, owner)
        return MethodType(self, instance)

    def bind_hook(self, instance, owner):
        pass
