# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

class framework_builder(type):
    """Metaclass for BaseFramework."""

    def __new__(cls, clsname, bases, clsdict):
        if bases != (object,):  # meaning: cls is subclass of BaseFramework
            field_names = [
                name for name, descriptor in clsdict.items()
                if isinstance(descriptor, BaseField)
            ]
            clsdict['_field_names'] = field_names
        clsobj = super().__new__(cls, clsname, bases, clsdict)
        return clsobj


class BaseFramework(object, metaclass=framework_builder):
    """Defines the framework for one particular type of exercise."""

    def __init__(self, *arg, **field_values):
        if arg:
            raise ValueError(
                "expected no positional argument for framework initialization"
            )
        for name, value in field_values.items():
            if name not in self._field_names:
                raise ValueError(f"unknown data attribute called {name}")
            setattr(self, name, value)
        self.framework_validate()

    def framework_validate(self):
        """Framework-level validation: to be overriden by subclasses.

        This method is called once all field-level values are assigned. This
        is to make sure that the entire exercise framework makes sense as a
        whole.

        This method produces no result when the data validation passes;
        otherwise, it raises an Exception if there is something wrong.
        """
        pass


class BaseField(object):
    """Field descriptor of framework classes.

    It uses __dict__ of the host instance object to store the actual data.
    """

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.field_name]

    def __set__(self, instance, value):
        if self.field_name in instance.__dict__:
            raise AttributeError("reassigning field data is not allowed")
        self.field_validate(value)
        instance.__dict__[self.field_name] = value

    def __delete__(self, instance):
        raise AttributeError("deleting field data is not allowed")

    def __set_name__(self, owner, field_name):
        if not issubclass(owner, BaseFramework):
            raise TypeError(
                f"field '{field_name}' should have been defined in "
                f"subclasses of BaseFramework"
            )
        self.field_name = field_name

    def field_validate(self, value):
        """Field value assignment validation: to be overriden by subclasses.

        This method is called when there is an assignment of value to the field
        of host instance object to ensure the integrity of assigned value.

        This method produces no result when the data validation passes;
        otherwise, it raises an Exception if there is something wrong.
        """
        pass
