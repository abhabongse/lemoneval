# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>
"""Parameter classes for each attribute in exercise frameworks."""

from ..utils.argdefault import ArgumentDefault
_argdefault = ArgumentDefault()  # empty placeholder


class BaseParameter(object):
    """Parameter descriptor for framework classes.

    This descriptor does not allow reassignment of values once it is assigned
    for the first time. It also validates the data before assignment with the
    method parameter_validate.

    It uses __dict__ of the host instance to store the actual data.
    """

    __slots__ = ("name",)

    def __init__(self, *, name=_argdefault):
        self.name = name

    def __set_name__(self, owner, name):
        self.name = self.name or name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if self.name in instance.__dict__:
            raise AttributeError("reassigning parameter is not allowed")
        instance.__dict__[self.name] = self.parameter_validate(value)

    def __delete__(self, instance):
        raise AttributeError("deleting parameter is not allowed")

    def parameter_validate(self, value):
        """Parameter assignment validation: to be overriden by subclasses.

        This method is called when there is an assignment of value to the
        parameter of host instance to ensure the integrity of assigned value.

        This method returns the sanitized value when the validation is
        successful; otherwise, it raises an exception describing what went
        wrong.
        """
        return value


class DataTypeMixin(BaseParameter):
    """Parameter mixin class for parameter data type support."""

    def __init__(self, *, dtype=_argdefault, **kwargs):
        super().__init__(**kwargs)
        if dtype is _argdefault:
            return  # do nothing
        if not isinstance(dtype, type):
            raise TypeError("invalid dtype specified")
        self.dtype = dtype

    def check_dtype(self, value, raise_error=True):
        """Check the data type of the given value."""
        if hasattr(self, "dtype") and not isinstance(value, self.dtype):
            dtype = getattr(self.dtype, "__qualname__", self.dtype)
            if raise_error:
                raise TypeError(
                    f"expecting value type '{dtype}' for '{self.name}' but "
                    f"{value!r} is given"
                )
            return False
        return True


class DefaultValueMixin(BaseParameter):
    """Parameter mixin class for parameter default values."""

    def __init__(self, *, default=_argdefault, **kwargs):
        super().__init__(**kwargs)
        if default is not _argdefault:
            self.default = default


class ValidatorMixin(BaseParameter):
    """Parameter mixin class to add parameter validation support."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators = []

    def add_validators(self, *validators):
        """Attach a sequence of validators to the parameter. Each validator
        will be run against a single value argument when it is assigned to the
        parameter.

        A validator could be an object of BaseValidator type or any callable
        which expects one value argument. If the value is considered valid by
        the validator, then it should return True. Otherwise, it should either
        return False or raise an exception describing what went wrong.
        """
        from .validators import BaseValidator, PredicateValidator
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

    def add_validator(self, validator):
        """This method is the same as add_validators except that only one
        validator may be given at a time.

        This method will return the validator itself so it could be used as a
        decorator for a staticmethod validator in framework classes. It will
        automatically be wrapped by @staticmethod upon return.
        """
        self.add_validators(validator)
        return staticmethod(validator)

    def check_with_validators(self, value, raise_error=True):
        """Run validators against the given value."""
        for validator in self.validators:
            if not validator(value, self.name):
                if raise_error:
                    raise ValueError(
                        f"the given value {value!r} failed the validation "
                        f"for '{self.name}'"
                    )
                return False
        return True


class Parameter(ValidatorMixin, DefaultValueMixin,
                DataTypeMixin, BaseParameter):
    """Single-value parameter descriptor for exercise framework."""

    def __init__(self, *, name=_argdefault, dtype=_argdefault,
                    default=_argdefault):
        super().__init__(name=name, dtype=dtype, default=default)

    def parameter_validate(self, value):
        self.check_dtype(value)
        self.check_with_validators(value)
        return value


class SequenceParameter(Parameter):
    """Sequence of parameters descriptor for exercise framework.

    This is similar to Parameter, except that it is a sequence of values
    rather than a single value.

    Lower bound and upper bound lengths (denoted as 'lb_length' and
    'ub_length' respectively) can be provided through the keyword 'length'
    to limit the length of sequence in this parameter. The 'length' could
    be specified as a single integer (meaning the sequence has such fixed
    length), or an iterable of size 1 or 2. In this latter case, the first
    and the second integer of the iterable provides the lower bound and the
    upper bound limit on the sequence length, respectively. If the second
    integer is missing, then there is no upper bound limit.
    """

    __slots__ = ("lb_length", "ub_length")

    def __init__(self, *, name=_argdefault, dtype=_argdefault,
                    default=_argdefault, length=(0,)):
        super().__init__(name=name, dtype=dtype, default=default)
        self.lb_length, self.ub_length = self._resolve_lengths(length)

    def parameter_validate(self, values):
        length, values = self.sanitize_values(values)
        self.check_sequence_length(length)
        for index, value in enumerate(values):
            try:
                self.check_dtype(value)
                self.check_with_validators(value)
            except Exception as e:
                raise ValueError(
                    f"error for value at index {index} of parameter "
                    f"sequence '{self.name}'"
                ) from e
        return values

    @staticmethod
    def _resolve_lengths(length):
        """Process the length input.

        The 'length' could be specified as a single integer (meaning the
        sequence has such fixed length), or an iterable of size 1 or 2. In this
        latter case, the first and the second integer of the iterable provides
        the lower bound and the upper bound limit on the sequence length,
        respectively. If the second integer is missing, then there is no upper
        bound limit."""
        from math import inf as INF
        if isinstance(length, int):
            if length < 0:
                raise ValueError(
                    f"'length' should be a non-negative interger but "
                    f"{length} is given"
                )
            return length, length
        try:
            size = len(length); length = tuple(length)
        except TypeError as e:
            raise TypeError(
                f"'length' must be an integer or an iterable of 1 or 2 "
                f"integers",
            ) from e
        if not 1 <= len(length) <= 2:
            raise ValueError(
                f"expected an iterable 'length' of size 1 or 2, but one of "
                f"size {size} was given"
            )
        if not all(isinstance(l, int) for l in length):
            raise TypeError(
                f"lower & upper bound limit of 'length' must be "
                f"integers but {length} was given"
            )
        if length[0] < 0:
            raise ValueError(
                f"lower bound of 'length' should be a non-negative "
                f"interger but {length[0]} is given"
            )
        if len(length) == 1:
            return length[0], INF
        if length[0] > length[1]:
            raise ValueError(
                f"lower bound of 'length' cannot be greater than upper bound "
                f"but {length} were given"
            )
        return length

    def sanitize_values(self, values):
        """Sanitize the values container by obtaining the finite length of
        the container and convert it to a tuple sequence."""
        try:
            length = len(values)  # make sure it is finitely countable
            values = tuple(values)  # works if iterable
        except TypeError as e:
            raise TypeError(
                f"the values for '{self.name}' must be an iterable of finite "
                f"length"
            ) from e
        return length, values

    def check_sequence_length(self, length):
        """Check if the length of the tuples is within the bounds."""
        if not self.lb_length <= length <= self.ub_length:
            if self.lb_length == self.ub_length:
                raise ValueError(
                    f"expecting '{self.name}' of length {self.lb_length} but "
                    f"one of length {length} was given"
                )
            import math
            if self.ub_length == math.inf:
                raise ValueError(
                    f"expecting '{self.name}' of length at least "
                    f"{self.lb_length} but one of length {length} was given"
                )
            raise ValueError(
                f"expecting '{self.name}' of length between {self.lb_length} "
                f"and {self.ub_length} but one of length {length} was given"
            )
