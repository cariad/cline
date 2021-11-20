from argparse import ArgumentParser
from typing import IO, Protocol


class CliProtocol(Protocol):
    @property
    def app_version(self) -> str:
        """
        Gets the host application version.
        """

    @property
    def arg_parser(self) -> ArgumentParser:
        """
        Gets the argument parser.
        """

    @property
    def out(self) -> IO[str]:
        """
        Gets `stdout` or equivalent output writer.
        """
