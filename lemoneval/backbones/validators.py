# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>
"""Validator classes for each parameter in exercise frameworks."""


class BaseValidator(object):
    """Defines a callable object which checks if the given value is valid."""

    __slots__ = ("name",)

    def __init__(self, *, name=None):
        self.name = name

    def __call__(self, value, target):
        """Checks whether the value is valid. If the validation is successful
        then True is returned. Otherwise, either False is returned or an
        exception describing what went wrong is raised.

        Target is the name of the object requiring the validation and it is
        used for error messages in exceptions.
        """
        pass


class PredicateValidator(BaseValidator):
    """Checks whether the given values passes the predicate test."""

    __slots__ = ("predicate",)

    def __init__(self, predicate, *, name=None):
        if name is None:
            name = getattr(predicate, "__qualname__", None)
        super().__init__(name=name)
        self.predicate = predicate

    def __call__(self, value, target):
        try:
            if self.predicate(value):
                return True
            else:
                raise ValueError
        except Exception as e:
            test_name = self.name or "the predicate test"
            raise ValueError(
                f"the given value {value!r} failed {test_name} for the "
                f"parameter '{target}'"
            ) from e
