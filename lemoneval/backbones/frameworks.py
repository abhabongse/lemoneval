# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>
"""Exercise framework is the core structure of what one type of exercise could
be. Custom frameworks are expected to be derived from `BaseFramework`. See
examples of custom frameworks in modules under `lemoneval.assembled`.
"""

from inspect import getfullargspec, Signature, Parameter


class _framework_builder(type):
    """A metaclass for `BaseFramework` and its subclasses."""

    def __init__(cls, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)
        cls._extract_parameter_names(clsdict)
        cls._make_signature()

    def _extract_parameter_names(cls, clsdict):
        """Create `parameter_names` from `clsdict` for framework class."""
        old_parameter_names = getattr(cls, "parameter_names", ())
        new_parameter_names = []
        from .parameters import BaseParameter
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
        cls.parameter_names = old_parameter_names + tuple(new_parameter_names)

    def _make_signature(cls):
        """Create `inspect.Signature` object for framework class."""
        parameters = []
        for name in cls.parameter_names:
            parameter_object = getattr(cls, name)
            default = getattr(parameter_object, "default", Parameter.empty)
            annotation = getattr(
                parameter_object, "annotation", Parameter.empty
            )
            parameters.append(Parameter(
                name, Parameter.KEYWORD_ONLY,
                default=default, annotation=annotation
            ))
        cls.__signature__ = Signature(parameters)


class BaseFramework(object, metaclass=_framework_builder):
    """Defines structural framework for one type of exercise format.

    Caution:
        Parameter values will be written to `__dict__` of the instance object.
        Avoid directly interacting with `__dict__` if possible.
    """

    # This attribute is used by '..util.json' package to facilitate JSON
    # serialization.
    serialized_kwargs = "__dict__"

    def __init__(self, *args, **parameters):
        """To initialize an instance of the framework, all framework-specific
        parameters must be provided via keyword-only arguments through the
        constructor.
        """
        self._validate_and_set_parameters(parameters)
        self.framework_validate()  # QUESTION: move to sub of above call?

    def __repr__(self):
        parameters_text = ",\n".join(
            f"  {name}={getattr(self, name)!r}"
            for name in self.parameter_names
        )
        return f"{type(self).__qualname__}(\n{parameters_text}\n)"

    def _validate_and_set_parameters(self, parameters):
        """Verify the provided parameters and store them in instance object.

        This method first verifies that all parameters are provided and they
        are valid according to parameter-level specifications. Errors will be
        raised upon validation errors.

        Superflous parameters are silently ignored.
        """
        for name in self.parameter_names:
            if name not in parameters:
                raise ValueError(f"missing parameter '{name}'")
            setattr(self, name, parameters[name])

    def framework_validate(self):
        """Framework-level validation: to be overriden by subclasses.

        This method is called once all parameter-level values are assigned and
        validated. It is to make sure that the entire exercise framework is
        valids as a whole.

        This method should return nothing when the validation succeeds;
        otherwise, it should raised an exception describing what went wrong.
        """
        pass

    def create_session(self):
        """Create an exercise session from this exercise framework.

        When an exercise performer is attempting at the exercise, a session
        for this framework is created with this method.
        """
        from .sessions import Session
        return Session(self)

    def __iter__(self):
        return self.create_session()

    def resume_session(self, session):
        """Resume the session to the next step using the given responses.

        Warning:
            While this method is expected to be overriden by subclasses, it is
            intended to be called by the internals of the Session object
            instances without direct external intervention.

        Implementers of this method is expected to interact with `session`
        object to read and modify the state of the session. For instance,
        if the performer's interactions with sessionobject are divided into
        *phases*, then an implementer may opt to create `session.phase_counter`
        attribute to keep track of that fact.

        The package `.phases` provides linear-stage (LS) phasing as well as
        deterministic finite state machine (DFSM) phasing to help implement
        this method. Otherwise, please keep in mind the following details.

        Important detail:
            The first call to this method by a Session instance will be made
            with empty response. This step can be used to set up a new
            exercise session.

        Another important detail:
            Once no more responses is expected from the performer, the
            attribute `session.report` must be defined with the end summary
            of the session, and `StopIteration` must be raised.
        """
        raise NotImplementedError
