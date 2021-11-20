from abc import ABC, abstractproperty
from argparse import ArgumentParser
from functools import cached_property
from logging import basicConfig, getLogger, root
from sys import argv, stdout
from typing import IO, List, Optional, Type, Union

from cline.cli_protocol import CliProtocol
from cline.command_line_arguments import CommandLineArgs
from cline.exceptions import (
    CannotMakeArguments,
    NoAvailableTasks,
    UserNeedsHelp,
    UserNeedsVersion,
)
from cline.tasks import AnyTask, HelpTask, VersionTask


class Cli(ABC, CliProtocol):
    def __init__(
        self,
        args: Optional[List[str]] = None,
        out: Optional[IO[str]] = None,
        app_version: str = "",
    ) -> None:
        self._args = args or argv[1:]
        self._logger = getLogger("cline")
        self._out = out or stdout
        self._app_version = app_version
        self._logger.debug("%s initialised", self.__class__)

    @property
    def app_version(self) -> str:
        """
        Gets the host application version.
        """

        return self._app_version

    @abstractproperty
    def parser(self) -> ArgumentParser:
        """
        Gets the argument parser.
        """

    @cached_property
    def args(self) -> CommandLineArgs:
        """
        Gets the parsed command line arguments.
        """

        known, unknown = self.parser.parse_known_args(self._args)
        args = CommandLineArgs()
        args.add_namespace(known)
        args.add_unknown(unknown)
        return args

    @property
    def out(self) -> IO[str]:
        """
        Gets `stdout` or equivalent output writer.
        """

        return self._out

    @property
    def task(self) -> AnyTask:
        """
        Gets the task for this CLI to perform.
        """

        tasks: List[Type[AnyTask]] = [
            *self.tasks,
            HelpTask,
        ]

        if self._app_version:
            tasks.append(VersionTask)

        tasks.append(HelpTask)

        for task in tasks:
            try:
                self._logger.debug("asking %s to make arguments", task)
                args = task.make_args(self.args)
                self._logger.debug("%s made arguments", task)
                break
            except (CannotMakeArguments, CannotMakeArguments):
                self._logger.debug("%s failed to make arguments", task)
                continue
        else:
            raise NoAvailableTasks

        return task(args=args, out=self.out)

    @abstractproperty
    def tasks(self) -> List[Type[AnyTask]]:
        """
        Gets the tasks that this CLI can perform.
        Ordered.
        """

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
            cli.out.write(cli.parser.format_help())
            if ex.explicit:
                exit(0)
            exit(1)
        except UserNeedsVersion:
            cli.out.write(cli.app_version)
            cli.out.write("\n")
            exit(0)

        exit(exit_code)
