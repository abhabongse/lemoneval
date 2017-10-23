# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

class BaseParameter(object):
    """Parameter descriptor for framework classes.

    This descriptor does not allow reassignment of values once it is assigned
    for the first time. It also validates the data before assignment with the
    method parameter_validate.

    It uses __dict__ of the host instance to store the actual data.
    """

    __slots__ = ("name",)

    def __init__(self, *, name=None):
        self.name = name

    def __set_name__(self, owner, name):
        self.name = self.name or name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if self.name in instance.__dict__ :
            raise AttributeError("reassigning parameter is not allowed")
        self.parameter_validate(value)
        instance.__dict__[self.name] = value

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


class Parameter(BaseParameter):
    """Single-value parameter descriptor for exercise framework."""

    __slots__ = ("dtype", "validators")

    def __init__(self, *, dtype=object, name=None):
        self.dtype = dtype  # expected type of parameter
        self.validators = []
        super().__init__(name=name)

    def add_validators(self, *validators):
        """Attach a sequence of validators to the parameter. Each validator
        will be run against a single value argument when it is assigned to the
        parameter.

        A validator could be an object of BaseValidator type or any callable
        which expects one value argument. If the value is considered valid by
        the validator, then it should return True. Otherwise, it should either
        return False or raise an exception describing what went wrong.
        """
        from .validator import BaseValidator, PredicateValidator
        for validator in validators:
            if isinstance(validator, BaseValidator):
                self.validators.append(validator)
            elif callable(validator):
                self.validators.append(PredicateValidator(validator))
            else:
                alien = getattr(validator, "__qualname__", validator)
                raise TypeError(
                    f"expected a validator but {alien} was given"
                )

    def parameter_validate(self, value):
        if not isinstance(value, self.dtype):
            dtype = getattr(self.dtype, "__qualname__", self.dtype)
            raise TypeError(
                f"expecting value type '{dtype}' for the parameter "
                f"'{self.name}' but {value!r} is given"
            )
        for validator in self.validators:
            if not validator(value, self.name):
                raise ValueError(
                    f"the given value {value!r} failed the validation"
                )
