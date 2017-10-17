# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from .base import BaseField


class TextField(BaseField):
    """Text field variant of fields."""

    def check_valid(self, value):
        return isinstance(value, str)


class IntegerField(BaseField):
    """Integer field variant of fields."""

    def check_valid(self, value):
        return isinstance(value, int)
