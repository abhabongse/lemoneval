# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>
"""Decorator helpers."""

from functools import update_wrapper


class CallableWrapper(object):
    """Decorator which allows injection into decorated object method.

    This class takes in an object method (a function) and wraps it inside a
    new callable proxy method. Whenever this proxy method is binded to an
    instance object, the method `update_method` will always be called.

    One usage of `update_method` of this class is to call update the callable
    proxy method with `functools.update_wrapper` to provide a more accurate
    docstrings, signatures, etc.
    """

    def __init__(self, func):
        self._func = func
        update_wrapper(self, func, updated=())

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        self.update_method(instance)
        from types import MethodType
        return MethodType(self, instance)

    def update_method(self, instance):
        pass
