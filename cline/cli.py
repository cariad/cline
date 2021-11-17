from abc import ABC, abstractproperty
from argparse import ArgumentParser
from functools import cached_property
from logging import basicConfig, getLogger, root
from sys import argv, stdout
from typing import IO, Any, List, Optional, Type, Union

from cline.base_tasks import Task
from cline.command_line_arguments import CommandLineArguments
from cline.exceptions import (
    CannotMakeArguments,
    CommandLineArgumentError,
    NoAvailableTasks,
)
from cline.tasks import HelpTask, VersionTask
from cline.types import CliTaskConfig

AnyTask = Task[Any]


class Cli(ABC):
    def __init__(
        self,
        args: Optional[List[str]] = None,
        out: Optional[IO[str]] = None,
        version: Optional[str] = None,
    ) -> None:
        self._args = args or argv[1:]
        self._logger = getLogger("cline")
        self._out = out or stdout
        self._version = version
        self._logger.debug("%s initialised", self.__class__)

    @abstractproperty
    def arg_parser(self) -> ArgumentParser:
        """
        Gets an argument parser.
        """

    @cached_property
    def args(self) -> CommandLineArguments:
        """
        Gets the parsed command line arguments.
        """

        known, unknown = self.arg_parser.parse_known_args(self._args)
        args = CommandLineArguments()
        args.add_namespace(known)
        args.add_unknown(unknown)
        return args

    @property
    def task(self) -> AnyTask:
        """
        Gets the task for this CLI to perform.
        """

        tasks: List[Type[AnyTask]] = [
            *self.tasks,
            HelpTask,
        ]

        if self._version:
            tasks.append(VersionTask)

        tasks.append(HelpTask)

        for task in tasks:
            try:
                self._logger.debug("asking %s to make arguments", task)
                args = task.make_task_args(self.args)
                self._logger.debug("%s made arguments", task)
                break
            except CommandLineArgumentError or CannotMakeArguments:
                self._logger.debug("%s failed to make arguments", task)
                continue
        else:
            raise NoAvailableTasks

        config = CliTaskConfig(
            exception_exit_code=self.exception_exit_code,
            out=self._out,
            render_help=self.render_help,
            version=self._version,
        )
        return task(args=args, config=config)

    def render_help(self) -> None:
        self._out.write(self.arg_parser.format_help())

    @abstractproperty
    def tasks(self) -> List[Type[AnyTask]]:
        """
        Gets the tasks that this CLI can perform.
        Ordered.
        """

    @property
    def exception_exit_code(self) -> int:
        """
        Gets the exit code to return when an exception occurs. Override to
        change.
        """

        return 127

    @classmethod
    def invoke_and_exit(
        cls,
        init_logging: bool = True,
        log_level: Optional[Union[int, str]] = None,
        version: Optional[str] = None,
    ) -> None:
        if init_logging:
            fmt = "%(levelname)s • %(name)s • %(pathname)s:%(lineno)d • %(message)s"
            # extra_dict = {'className': 'NameOfClass'}
            # logger = logging.getLogger('logger_name')

            basicConfig(format=fmt)

        if log_level is not None:
            root.setLevel(log_level)

        cli = cls(version=version)
        exit_code = cli.task.safe_invoke()
        exit(exit_code)
