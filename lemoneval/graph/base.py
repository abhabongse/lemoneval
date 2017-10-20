# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

class framework_builder(type):
    """Metaclass for BaseFramework and its subclasses."""

    def __new__(cls, clsname, bases, clsdict):
        if bases == (object,):
            # meaning: cls is not subclass of BaseFramework
            return super().__new__(cls, clsname, bases, clsdict)
        clsdict['parameter_names'] = tuple(
            name for name, descriptor in clsdict.items()
            if isinstance(descriptor, BaseParameter)
        )
        clsobj = super().__new__(cls, clsname, bases, clsdict)
        return clsobj


class BaseFramework(object, metaclass=framework_builder):
    """Defines the structural framework for one type of exercise.

    Caution: Parameter values will be written to the __dict__ of the instance
    object. Please do not meddle with __dict__ itself like a responsible user.
    """

    def __init__(self, **parameters):
        self.set_parameters(parameters)
        self.framework_validate()

    def __repr__(self):
        parameters_text = ",\n".join(
            f"    {name}={getattr(self, name)!r}"
            for name in self.parameter_names
        )
        return f"{type(self).__qualname__}(\n{parameters_text}\n)"

    def set_parameters(self, parameters):
        """Check that all expected parameters are provided and store them.
        Excessive unwanted parameters will be ignored.
        """
        for name in self.parameter_names:
            if name not in parameters:
                raise ValueError(f"missing parameter: {name}")
            setattr(self, name, parameters[name])

    def framework_validate(self):
        """Framework-level validation: to be overriden by subclasses.

        This method is called once all parameter-level values are assigned and
        validated. It is to make sure that the entire exercise framework makes
        sense as a whole.

        This method produces no result when the validation is successful;
        otherwise, it raises an exception describing what went wrong.
        """
        pass


class BaseParameter(object):
    """Parameter descriptor for framework classes.

    This descriptor does not allow reassignment of values once it is assigned
    for the first time. It also validates the data before assignment with the
    method parameter_validate.

    It uses __dict__ of the host instance to store the actual data.
    """

    def __set_name__(self, owner, parameter_name):
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
