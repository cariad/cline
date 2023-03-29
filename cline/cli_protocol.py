from typing import IO, Generic, Protocol, TypeVar

TParser = TypeVar("TParser", covariant=True)


class CliProtocol(Protocol, Generic[TParser]):
    @property
    def app_version(self) -> str:
        """
        Gets the host application version.
        """

    @property
    def out(self) -> IO[str]:
        """
        Gets `stdout` or equivalent output writer.
        """

    @property
    def parser(self) -> TParser:
        """
        Gets the argument parser.
        """
