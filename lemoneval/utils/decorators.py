# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>

class MethodWrapper(object):
    """Decorator which turns a method into an updatable one."""

    def __init__(self, func):
        self._func = func

    def __call__(self, instance, *args, **kwargs):
        return self._func(instance, *args, **kwargs)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        self.update_method(instance)
        from types import MethodType
        return MethodType(self, instance)

    def update_method(self, instance):
        pass
