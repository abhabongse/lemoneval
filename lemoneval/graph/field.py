# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from .base import BaseField


class TextField(BaseField):
    """Text field variant of fields."""

    def field_validate(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f"expecting a string for the field {self.field_name}, "
                f"but given: {value!r}"
            )


class IntegerField(BaseField):
    """Integer field variant of fields."""

    def field_validate(self, value):
        if not isinstance(value, int):
            raise TypeError(
                f"expecting an integer for the field {self.field_name}, "
                f"but given: {value!r}"
            )
