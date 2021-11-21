from abc import ABC, abstractmethod
from typing import IO, Any, Generic, Type, TypeVar

from cline.cli_args import CommandLineArguments
from cline.exceptions import UserNeedsHelp, UserNeedsVersion

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
    def make_args(cls, args: CommandLineArguments) -> TTaskArgs:
        """
        Makes and returns strongly-typed arguments for this task based on the
        parsed command line arguments `args`.

        Arguments:
            args: Parsed command line arguments

        Raises:
            CannotMakeArguments: If the given arguments are not relevant to this
            task

        Returns:
            Task arguments
        """

    @abstractmethod
    def invoke(self) -> int:
        """
        Invokes the task.

        Reads arguments from `self.args`. Writes output to `self.out`.

        Returns the shell exit code.
        """

    def safe_invoke(
        self,
    ) -> int:
        try:
            return self.invoke()
        except KeyboardInterrupt:
            return 100
        except (UserNeedsHelp, UserNeedsVersion):
            raise
        except Exception as ex:
            self.out.write("🔥 ")
            self.out.write(str(ex))
            self.out.write("\n")
            return 101


AnyTask = Task[Any]
AnyTaskType = Type[AnyTask]
