# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

class BaseField(object):
    """Base field descriptor to be used by exercise classes."""

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.field_name]

    def __set__(self, instance, value):
        if not self.check_valid(value):
            raise ValueError(f"cannot assign '{value}' to the field '{self.field_name}'")
        instance.__dict__[self.field_name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.field_name]

    def __set_name__(self, owner, field_name):
        if not issubclass(owner, BaseExercise):
            raise TypeError(f"field '{field_name}' should have been defined in subclasses of BaseExercise")
        self.field_name = field_name

    def check_valid(self, value):
        return True


class exercise_builder(type):
    def __new__(cls, clsname, bases, clsdict):
        field_names = [
            name for name, descriptor in clsdict.items()
            if isinstance(descriptor, BaseField)
        ]
        clsdict['_field_names'] = field_names
        clsobj = super().__new__(cls, clsname, bases, clsdict)
        return clsobj


class BaseExercise(object, metaclass=exercise_builder):
    def __init__(self, *arg, **field_values):
        if arg:
            raise ValueError("expected no positional argument for initialization")
        for name, value in field_values.items():
            if name not in self._field_names:
                raise ValueError(f"unknown data attribute '{name}'")
            setattr(self, name, value)
        self.selfcheck_valid()

    def selfcheck_valid(self):
        pass
