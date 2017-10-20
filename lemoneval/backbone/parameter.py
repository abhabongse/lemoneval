# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from numbers import Real

class BaseParameter(object):
    """Parameter descriptor for framework classes.

    This descriptor does not allow reassignment of values once it is assigned
    for the first time. It also validates the data before assignment with the
    method parameter_validate.

    It uses __dict__ of the host instance to store the actual data.
    """

    def __set_name__(self, owner, parameter_name):
        from .framework import BaseFramework
        if not issubclass(owner, BaseFramework):
            raise TypeError(
                f"parameter {parameter_name} should have been defined in "
                f"subclasses of BaseFramework"
            )
        self.parameter_name = parameter_name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.parameter_name]

    def __set__(self, instance, value):
        if self.parameter_name in instance.__dict__ :
            raise AttributeError("reassigning parameter is not allowed")
        self.parameter_validate(value)
        instance.__dict__[self.parameter_name] = value

    def __delete__(self, instance):
        raise AttributeError("deleting parameter is not allowed")

    def parameter_validate(self, value):
        """Parameter assignment validation: to be overriden by subclasses.

        This method is called when there is an assignment of value to the
        parameter of host instance to ensure the integrity of assigned value.

        This method produces no result when the validation is successful;
        otherwise, it raises an exception describing what went wrong.
        """
        pass


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
