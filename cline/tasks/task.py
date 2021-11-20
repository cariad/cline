from abc import ABC, abstractmethod
from typing import IO, Any, Generic, Type, TypeVar

from cline.command_line_arguments import CommandLineArgs
from cline.exceptions import UserNeedsHelp

TTaskArgs = TypeVar("TTaskArgs")


class Task(ABC, Generic[TTaskArgs]):
    def __init__(self, args: TTaskArgs, out: IO[str]) -> None:
        self._args = args
        self._out = out

    @property
    def out(self) -> IO[str]:
        return self._out

    @property
    def args(self) -> TTaskArgs:
        return self._args

    @classmethod
    @abstractmethod
    def make_args(cls, args: CommandLineArgs) -> TTaskArgs:
        """Make args"""

    @abstractmethod
    def invoke(self) -> int:
        """
        Invokes the task.

        Returns the shell exit code.
        """

    def safe_invoke(
        self,
    ) -> int:
        try:
            return self.invoke()
        except KeyboardInterrupt:
            return 100
        except UserNeedsHelp:
            raise
        except Exception as ex:
            self.out.write("🔥 ")
            self.out.write(str(ex))
            self.out.write("\n")
            return 101


AnyTask = Task[Any]
AnyTaskType = Type[AnyTask]
