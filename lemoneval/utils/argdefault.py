# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>
"""Extension of NoneType for function argument placeholder."""

class ArgumentDefault():
    """Object to represent empty argument default which evaluates to False."""

    def __bool__(self):
        return False

EMPTY_DEFAULT = ArgumentDefault()
