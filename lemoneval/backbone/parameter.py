# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>

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
        if self.name in instance.__dict__:
            raise AttributeError("reassigning parameter is not allowed")
        instance.__dict__[self.name] = self.parameter_validate(value)

    def __delete__(self, instance):
        raise AttributeError("deleting parameter is not allowed")

    def parameter_validate(self, value):
        """Parameter assignment validation: to be overriden by subclasses.

        This method is called when there is an assignment of value to the
        parameter of host instance to ensure the integrity of assigned value.

        This method produces no result when the validation is successful;
        otherwise, it raises an exception describing what went wrong.
        """
        return value


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

    def add_validator(self, validator):
        """This method is the same as add_validators except that only one
        validator may be given at a time.

        This method will return the validator itself so it could be used as a
        decorator for a staticmethod validator in framework classes. It will
        automatically be wrapped by @staticmethod upon return.
        """
        self.add_validators(validator)
        return staticmethod(validator)

    def parameter_validate(self, value):
        if not isinstance(value, self.dtype):
            dtype = getattr(self.dtype, "__qualname__", self.dtype)
            raise TypeError(
                f"expecting value type '{dtype}' for '{self.name}' but "
                f"{value!r} is given"
            )
        for validator in self.validators:
            if not validator(value, self.name):
                raise ValueError(
                    f"the given value {value!r} failed the validation "
                    f"for '{self.name}'"
                )
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

    def __init__(self, *, length=(0,), dtype=object, name=None):
        self.lb_length, self.ub_length = self._resolve_lengths(length)
        super().__init__(dtype=dtype, name=name)

    def parameter_validate(self, values):
        try:
            length = len(values); values = tuple(values)
        except TypeError as e:
            e.args += (
                f"the values for '{self.name}' must be an iterable of finite "
                f"length",
            )
            raise
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
        for index, value in enumerate(values):
            if not isinstance(value, self.dtype):
                dtype = getattr(self.dtype, "__qualname__", self.dtype)
                raise TypeError(
                    f"expecting value type '{dtype}' for '{self.name}' but "
                    f"{value!r} (index: {index}) is given"
                )
            for validator in self.validators:
                if not validator(value, self.name):
                    raise ValueError(
                        f"the given value {value!r} (index: {index}) failed "
                        f"the validation for '{self.name}'"
                    )
        return values

    @staticmethod
    def _resolve_lengths(length):
        import math
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
            e.args += (
                f"'length' must be an integer or an iterable of one or two "
                f"integers",
            )
            raise
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
            return length[0], math.inf
        if length[0] > length[1]:
            raise ValueError(
                f"lower bound of 'length' cannot be greater than upper bound "
                f"but {length} were given"
            )
        return length
