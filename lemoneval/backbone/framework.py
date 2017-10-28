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
        clsdict['parameter_names'] = tuple(parameter_names)
        clsobj = super().__new__(cls, clsname, bases, clsdict)
        return clsobj


class BaseFramework(object, metaclass=framework_builder):
    """Defines the structural framework for one type of exercise.

    Caution: Parameter values will be written to the __dict__ of the instance
    object. Please do not meddle with __dict__ itself like a responsible user.
    """
    serializable_to_json = "__dict__"

    def __init__(self, *args, **parameters):
        self.set_parameters(parameters)
        self.framework_validate()

    def __repr__(self):
        parameters_text = ",\n".join(
            f"  {name}={getattr(self, name)!r}"
            for name in self.parameter_names
        )
        return f"{type(self).__qualname__}(\n{parameters_text}\n)"

    def set_parameters(self, parameters):
        """Check that all expected parameters are provided and store them.
        Excessive unwanted parameters will be ignored.
        """
        for name in self.parameter_names:
            if name not in parameters:
                raise ValueError(f"missing parameter '{name}'")
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

    def create_session(self):
        """When a player is attempted at the exercise, a session for the
        exercise framework must be created with this method.
        """
        from .session import Session
        return Session(self)
