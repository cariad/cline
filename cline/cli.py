from abc import ABC, abstractmethod, abstractproperty
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from functools import cached_property
from logging import basicConfig, getLogger, root
from sys import argv, stdout
from typing import IO, Any, Dict, Generic, List, Literal, Optional, Type, TypeVar, Union


class ClineError(Exception):
    pass


class CannotMakeArguments(ClineError):
    pass


class NoAvailableTasks(ClineError):
    pass


class CommandLineArgumentError(ClineError):
    pass


class MissingArgumentError(CommandLineArgumentError):
    pass


class UnexpectedArgumentTypeError(CommandLineArgumentError):
    pass


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


@dataclass
class CliTaskConfig:
    exception_exit_code: int
    out: IO[str]


TTaskArgs = TypeVar("TTaskArgs")


class Task(ABC, Generic[TTaskArgs]):
    def __init__(self, args: TTaskArgs, config: CliTaskConfig) -> None:
        self._args = args
        self._config = config

    @property
    def args(self) -> TTaskArgs:
        return self._args

    @classmethod
    @abstractmethod
    def make_task_args(cls, args: CommandLineArguments) -> TTaskArgs:
        """Make args"""

    @abstractmethod
    def invoke(self) -> int:
        """
        Invokes the task. Returns the shell exit code.
        """

    @property
    def out(self) -> IO[str]:
        return self._config.out

    def safe_invoke(self) -> int:
        try:
            return self.invoke()
        except KeyboardInterrupt:
            return self._config.exception_exit_code
        except Exception as ex:
            self.out.write("🔥 ")
            self.out.write(str(ex))
            self.out.write("\n")
            return self._config.exception_exit_code


class EagerTask(Task[Literal[None]]):
    @classmethod
    def make_task_args(cls, args: CommandLineArguments) -> Literal[None]:
        return None


class FlagTask(Task[Literal[None]]):
    @classmethod
    @abstractmethod
    def cli_flag(cls) -> str:
        """Make args"""

    @classmethod
    def make_task_args(cls, args: CommandLineArguments) -> Literal[None]:
        if not args.get_bool(cls.cli_flag()):
            raise CannotMakeArguments()


AnyTask = Task[Any]


class Cli(ABC):
    def __init__(
        self,
        args: Optional[List[str]] = None,
        out: Optional[IO[str]] = None,
    ) -> None:
        self._args = args or argv[1:]
        self._logger = getLogger("cline")
        self._out = out or stdout
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

        for task in self.tasks:
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
        )
        return task(args=args, config=config)

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
        log_level: Optional[int] = None,
    ) -> None:
        if init_logging:
            basicConfig()

        if log_level is not None:
            root.setLevel(log_level)

        cli = cls()
        exit_code = cli.task.safe_invoke()
        exit(exit_code)
