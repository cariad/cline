from argparse import Namespace
from typing import Dict, List, Union

from cline.exceptions import MissingArgumentError


class CommandLineArguments:
    def __init__(self) -> None:
        self._arguments: Dict[str, Union[str, bool, None]] = {}

    def add_namespace(self, namespace: Namespace) -> None:
        ns_dict = vars(namespace)
        for key in ns_dict:
            self._arguments[key] = ns_dict[key]

    def add_unknown(self, args: List[str]) -> None:
        for key in args:
            self._arguments[key] = None

    def get_bool(self, key: str) -> bool:
        """
        Raises:
            MissingArgument: raised if the argument is not set
            TypeError:       raised if the argument is not a bool
        """

        value = self._arguments.get(key, None)
        if not value:
            raise MissingArgumentError()
        if not isinstance(value, bool):
            raise TypeError()
        return value

    def get_string(self, key: str) -> str:
        """
        Raises:
            MissingArgument: raised if the argument is not set
            TypeError:       raised if the argument is not a string
        """

        value = self._arguments.get(key, None)
        if not value:
            raise MissingArgumentError()
        if not isinstance(value, str):
            raise TypeError()
        return value
