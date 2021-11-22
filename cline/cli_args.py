from typing import Dict, List, Optional, Union

from cline.exceptions import CannotMakeArguments

ArgumentsType = Dict[str, Union[str, bool, None]]


class CommandLineArguments:
    """
    Parsed command line arguments.

    Arguments:
        known:   Dictionary of known arguments.
        unknown: List of unknown arguments.
    """

    def __init__(
        self,
        known: Optional[ArgumentsType] = None,
        unknown: Optional[List[str]] = None,
    ) -> None:
        self._known = known or {}
        self._unknown = unknown or []

    def assert_string(self, key: str, value: str) -> None:
        """
        Asserts that the argument `key` has string value `value`.

        Raises `CannotMakeArguments` if the argument is not set or does not
        match.
        """

        if self.get_string(key) != value:
            raise CannotMakeArguments()

    def assert_true(self, key: str) -> None:
        """
        Asserts that the command line flag `key` is truthy.

        Raises `CannotMakeArguments` if the argument is not set, not a boolean
        or not truthy.
        """

        if not self.get_bool(key):
            raise CannotMakeArguments()

    def get_bool(self, key: str, default: Optional[bool] = None) -> bool:
        """
        Gets the command line argument `key` as a boolean.

        Returns `default` if the argument is not set but `default` is.

        Raises `CannotMakeArguments` if `default` is not set and the argument is
        not set or not a boolean.
        """

        value = self._known.get(key, None)

        if value is None and default is not None:
            return default
        if not isinstance(value, bool):
            raise CannotMakeArguments()
        return value

    def get_integer(self, key: str) -> int:
        """
        Gets the command line argument `key` as an integer.

        Raises `CannotMakeArguments` if the argument is not set or not an
        integer.
        """

        try:
            return int(self.get_string(key))
        except ValueError:
            raise CannotMakeArguments()

    def get_string(self, key: str) -> str:
        """
        Gets the command line argument `key` as a string.

        Raises `CannotMakeArguments` if the argument is not set or not a string.
        """

        value = self._known.get(key, None)
        if not isinstance(value, str):
            raise CannotMakeArguments()
        return value
