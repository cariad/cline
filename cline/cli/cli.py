from abc import ABC, abstractmethod, abstractproperty
from logging import basicConfig, getLogger, root
from sys import argv, stdout
from typing import IO, List, Optional, Type, Union

from cline.cli_args import CommandLineArguments
from cline.cli_protocol import CliProtocol, TParser
from cline.exceptions import (
    CannotMakeArguments,
    NoAvailableTasks,
    UserNeedsHelp,
    UserNeedsVersion,
)
from cline.tasks import AnyTask, AnyTaskType, HelpTask, VersionTask

RegisteredTasks = List[AnyTaskType]


class Cli(ABC, CliProtocol[TParser]):
    """
    Abstract base class for Cline entrypoints.

    Arguments:
        app_version: Host application version (defaults to empty)
        args:        Original command line arguments (defaults to argv)
        out:         stdout or equivalent output writer (defaults to stdout)
    """

    def __init__(
        self,
        app_version: str = "",
        args: Optional[List[str]] = None,
        out: Optional[IO[str]] = None,
    ) -> None:
        self._raw_args = args or argv[1:]
        self._cli_args: Optional[CommandLineArguments] = None
        self._logger = getLogger("cline")
        self._out = out or stdout
        self._app_version = app_version
        self._parser: Optional[TParser] = None
        self._tasks: Optional[List[AnyTaskType]] = None
        self._logger.debug("%s initialised", self.__class__)

    @property
    def app_version(self) -> str:
        """
        Gets the host application version.
        """

        return self._app_version

    @property
    def cli_args(self) -> CommandLineArguments:
        """
        Gets the parsed command line arguments.
        """

        if not self._cli_args:
            self._cli_args = self.make_cli_args(args=self._raw_args)
        return self._cli_args

    @abstractmethod
    def make_cli_args(self, args: List[str]) -> CommandLineArguments:
        """
        Parses `args` to make and return `CommandLineArguments`.

        Arguments:
            args: Command line arguments

        Returns:
            Parsed command line arguments
        """

    @abstractmethod
    def make_parser(self) -> TParser:
        """..."""

    @property
    def parser(self) -> TParser:
        """
        Gets the argument parser.
        """

        if not self._parser:
            self._parser = self.make_parser()
        return self._parser

    @property
    def out(self) -> IO[str]:
        """
        Gets `stdout` or equivalent output writer.
        """

        return self._out

    @abstractmethod
    def register_tasks(self) -> RegisteredTasks:
        """..."""

    @property
    def tasks(self) -> List[Type[AnyTask]]:

        if self._tasks is None:
            self._tasks = self.register_tasks()

            # If we know the host application's version then we can handle it:
            if self._app_version:
                self._tasks.append(VersionTask)

            # As an absolute fallback, we can always print help:
            self._tasks.append(HelpTask)

        return self._tasks

    @abstractproperty
    def help(self) -> str:
        """
        Gets CLI usage help.
        """

    @property
    def task(self) -> AnyTask:
        """
        Gets the task to perform.
        """

        # Walk through all the tasks in priority order, and use the first one
        # that's able to make sense of the command line arguments:
        for task in self.tasks:
            try:
                self._logger.debug("Asking %s to make arguments", task)
                args = task.make_args(self.cli_args)
                self._logger.debug("%s made arguments", task)
                break
            except (CannotMakeArguments, CannotMakeArguments):
                self._logger.debug("%s failed to make arguments", task)
                continue
        else:
            raise NoAvailableTasks()

        return task(args=args, out=self.out)

    @classmethod
    def invoke_and_exit(
        cls,
        init_logging: bool = True,
        log_level: Optional[Union[int, str]] = None,
        app_version: str = "",
    ) -> None:
        if init_logging:
            fmt = "%(levelname)s • %(name)s • %(pathname)s:%(lineno)d • %(message)s"
            basicConfig(format=fmt)

        if log_level is not None:
            root.setLevel(log_level)

        cli = cls(app_version=app_version)
        try:
            exit_code = cli.task.safe_invoke()
        except UserNeedsHelp as ex:
            cli.out.write(cli.help)
            if ex.explicit:
                exit(0)
            exit(1)
        except UserNeedsVersion:
            cli.out.write(cli.app_version)
            cli.out.write("\n")
            exit(0)

        exit(exit_code)
