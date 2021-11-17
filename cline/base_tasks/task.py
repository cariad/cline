from abc import ABC, abstractmethod
from typing import IO, Generic, TypeVar

from cline.command_line_arguments import CommandLineArguments
from cline.types import CliTaskConfig

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
