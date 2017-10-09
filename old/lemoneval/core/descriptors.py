# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
"""Collection of useful descriptors.
"""

class TypedDataDescriptor(object):
    """Data Descriptor which checks the type of value before storing.

    Attributes:
        value_type: Expected type to value to store
        name: Name of attribute this descriptor represents

    """
    def __init__(self, value_type, predicate=None):
        self.value_type = value_type
        self.predicate = predicate or (lambda x: True)

        if not isinstance(value_type, type):
            raise TypeError(f"expected type but {value!r} is given")
        if not callable(self.predicate):
            raise TypeError(f"predicate must be callable")

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.value_type):
            raise TypeError(f"expected {self.value_type.__qualname__} but "
                            f"{value!r} is given")
        if not self.predicate(value):
            raise ValueError(f"{value!r} did not satisfy attribute constraint")
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]

    def __set_name__(self, owner, name):
        self.name = name
