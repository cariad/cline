from argparse import Namespace
from typing import Dict, List, Optional, Union

from cline.exceptions import CannotMakeArguments

ArgumentsType = Dict[str, Union[str, bool, None]]


class CommandLineArgs:
    def __init__(self, args: Optional[ArgumentsType] = None) -> None:
        self._arguments = args or {}

    def add_namespace(self, namespace: Namespace) -> None:
        ns_dict = vars(namespace)
        for key in ns_dict:
            self._arguments[key] = ns_dict[key]

    def add_unknown(self, args: List[str]) -> None:
        for key in args:
            self._arguments[key] = None

    def assert_true(self, key: str) -> None:
        """
        Asserts that the command line flag `key` is truthy.

        Raises `CommandLineArgumentError` if the argument is not set, not a boolean or
        not truthy.
        """

        if not self.get_bool(key):
            raise CannotMakeArguments()

    def get_bool(self, key: str, default: Optional[bool] = None) -> bool:
        """
        Gets the command line argument `key` as a boolean.

        Returns `default` if the argument is not set but `default` is.

        Raises `CommandLineArgumentError` if `default` is not set and the argument is
        not set or not a boolean.
        """

        value = self._arguments.get(key, None)

        if value is None and default is not None:
            return default
        if not isinstance(value, bool):
            raise CannotMakeArguments()
        return value

    def get_integer(self, key: str) -> int:
        """
        Gets the command line argument `key` as an integer.

        Raises `CommandLineArgumentError` if the argument is not set or not an integer.
        """

        try:
            return int(self.get_string(key))
        except ValueError:
            raise CannotMakeArguments()

    def get_string(self, key: str) -> str:
        """
        Gets the command line argument `key` as a string.

        Raises `CommandLineArgumentError` if the argument is not set or not a string.
        """

        value = self._arguments.get(key, None)
        if not isinstance(value, str):
            raise CannotMakeArguments()
        return value
