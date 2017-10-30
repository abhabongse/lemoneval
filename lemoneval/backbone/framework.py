# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from itertools import chain


class framework_builder(type):
    """Metaclass for BaseFramework and its subclasses."""

    def __init__(cls, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)
        # Create parameter_names from clsdict
        old_parameter_names = getattr(cls, "parameter_names", ())
        new_parameter_names = []
        from .parameter import BaseParameter
        for name, descriptor in clsdict.items():
            if name in old_parameter_names:
                if not isinstance(descriptor, BaseParameter):
                    raise TypeError(
                        f"Parameter {name!r} overriden in derived class."
                    )
            elif isinstance(descriptor, BaseParameter):
                if name.startswith("_"):
                    raise NameError(
                        f"parameter names should not begin with an underscore "
                        f"but the name {name!r} is used"
                    )
                new_parameter_names.append(name)
        cls.parameter_names = tuple(chain(
            old_parameter_names, new_parameter_names
        ))


class BaseFramework(object, metaclass=framework_builder):
    """Defines the structural framework for one type of exercise.

    Caution: Parameter values will be written to the __dict__ of the instance
    object. Please do not meddle with __dict__ itself like a responsible user.
    """
    serialized_kwargs = "__dict__"

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

    def __iter__(self):
        return self.create_session()

    def progress_session(self, session, response):
        """Progress the session with the given response.

        For the first call, the response will always be an empty dictionary
        since there is no response yet.

        Once no more responses is expected, session.report must be defined with
        the summary of the session, and StopIteration must be raised.
        """
        session.report = {}
        raise StopIteration
