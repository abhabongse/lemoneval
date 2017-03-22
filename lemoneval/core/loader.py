# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
"""A helper tool to load a test root from a python config file."""

import importlib.util
from .graph import BaseNode

# Counter to assign to unique test configuration import
counter = 0

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
    global counter
    spec = importlib.util.spec_from_file_location(
        f'lemoneval.test_{counter}', config_path
        )
    counter += 1
    try:
        module = importlib.util.module_from_spec(spec)
    except AttributeError:
        raise ModuleNotFoundError(f'No test module at path: {config_path}')
    spec.loader.exec_module(module)
    try:
        root_test = module.ROOT_TEST
    except AttributeError:
        raise ImportError(f'Test module has no ROOT_TEST: {config_path}')
    if not isinstance(root_test, BaseNode):
        raise TypeError(f'ROOT_TEST has incorrect type: {config_path}')
    return root_test
