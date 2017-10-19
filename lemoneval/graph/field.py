# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from numbers import Real
from .base import BaseField


class TextField(BaseField):
    """Text field variant of fields."""

    def field_validate(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f"expecting a string for the field {self.field_name}, "
                f"but given: {value!r}"
            )


class NumberField(BaseField):
    """Generic (real) number field variant of fields."""

    def field_validate(self, value):
        if not isinstance(value, Real):
            raise TypeError(
                f"expecting a real number for the field {self.field_name}, "
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


class PositiveIntegerField(IntegerField):
    """Positive integer field variant of fields."""

    def field_validate(self, value):
        super().field_validate(value)
        if not value > 0:
            raise ValueError(
                f"integer must be positive for the field {self.field_name}, "
                f"but given: {value!r}"
            )
