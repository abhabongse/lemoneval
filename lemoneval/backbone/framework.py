# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

class framework_builder(type):
    """Metaclass for BaseFramework and its subclasses."""

    def __new__(cls, clsname, bases, clsdict):
        if bases == (object,):
            # meaning: cls is not subclass of BaseFramework
            return super().__new__(cls, clsname, bases, clsdict)
        from .parameter import BaseParameter
        parameter_names = []
        for name, descriptor in clsdict.items():
            if isinstance(descriptor, BaseParameter):
                if name.startswith("_"):
                    raise NameError(
                        f"parameter names should not begin with an underscore "
                        f"but the name {name!r} is used"
                    )
                parameter_names.append(name)
        clsdict['_parameter_names'] = tuple(parameter_names)
        clsobj = super().__new__(cls, clsname, bases, clsdict)
        return clsobj


class BaseFramework(object, metaclass=framework_builder):
    """Defines the structural framework for one type of exercise.

    Caution: Parameter values will be written to the __dict__ of the instance
    object. Please do not meddle with __dict__ itself like a responsible user.
    """

    def __init__(self, **parameters):
        self._set_parameters(parameters)
        self._framework_validate()

    def __repr__(self):
        parameters_text = ",\n".join(
            f"    {name}={getattr(self, name)!r}"
            for name in self._parameter_names
        )
        return f"{type(self).__qualname__}(\n{parameters_text}\n)"

    def _set_parameters(self, parameters):
        """Check that all expected parameters are provided and store them.
        Excessive unwanted parameters will be ignored.
        """
        for name in self._parameter_names:
            if name not in parameters:
                raise ValueError(f"missing parameter '{name}'")
            setattr(self, name, parameters[name])

    def _framework_validate(self):
        """Framework-level validation: to be overriden by subclasses.

        This method is called once all parameter-level values are assigned and
        validated. It is to make sure that the entire exercise framework makes
        sense as a whole.

        This method produces no result when the validation is successful;
        otherwise, it raises an exception describing what went wrong.
        """
        pass