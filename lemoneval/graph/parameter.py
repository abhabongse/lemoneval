# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from numbers import Real
from .base import BaseParameter


class TextParameter(BaseParameter):
    """Text parameter descriptor for exercise framework."""

    def parameter_validate(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f"expecting a string for the parameter "
                f"{self.parameter_name}, but instead given: {value!r}"
            )


class NumberParameter(BaseParameter):
    """Generic (real) number parameter descriptor for exercise framework."""

    def parameter_validate(self, value):
        if not isinstance(value, Real):
            raise TypeError(
                f"expecting a real number for the parameter "
                f"{self.parameter_name}, but instead given: {value!r}"
            )


class IntegerParameter(BaseParameter):
    """Integer parameter descriptor for exercise framework."""

    def parameter_validate(self, value):
        if not isinstance(value, int):
            raise TypeError(
                f"expecting an integer for the parameter "
                f"{self.parameter_name}, but instead given: {value!r}"
            )


class PositiveIntegerParameter(IntegerParameter):
    """Positive integer parameter descriptor for exercise framework."""

    def parameter_validate(self, value):
        super().parameter_validate(value)
        if not value > 0:
            raise ValueError(
                f"integer must be positive for the parameter "
                f"{self.parameter_name}, but instead given: {value!r}"
            )
