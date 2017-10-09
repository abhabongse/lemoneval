# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
"""A helper tool to load a test root from a python config file."""

import importlib.util
import pathlib
from .graph import BaseNode


def load_test(config_path):
    """Return the root of the test graph in the configuration file.

    Args:
        config_path: Path to configuration file containing `ROOT_TEST`
            variable of type `BaseNode`

    Return:
        A `BaseNode` object which is the root of the entire test.

    Raises:
        ModuleNotFoundError: If the given config path is not found
        AttributeError: If the config file does not contain `ROOT_TEST`
        TypeError: If ROOT_TEST is not of the type `BaseNode`

    """
    config_path = pathlib.Path(config_path).absolute()
    cleaned_config_path = str(config_path).replace('/', '_')
    name = f"lemoneval.test_{cleaned_config_path}"
    spec = importlib.util.spec_from_file_location(name, config_path)
    try:
        module = importlib.util.module_from_spec(spec)
    except AttributeError:
        raise ModuleNotFoundError(f"no test module at path {config_path!r}")
    spec.loader.exec_module(module)
    try:
        root_test = module.ROOT_TEST
    except AttributeError:
        raise ImportError(f"no ROOT_TEST in test module {config_path!r}")
    if not isinstance(root_test, BaseNode):
        raise TypeError(
            f"ROOT_TEST has incorrect type in test module {config_path!r}"
            )
    return root_test
