from abc import abstractmethod
from typing import Literal

from cline.base_tasks.task import Task
from cline.command_line_arguments import CommandLineArguments
from cline.exceptions import CannotMakeArguments


class FlagTask(Task[Literal[None]]):
    @classmethod
    @abstractmethod
    def cli_flag(cls) -> str:
        """Make args"""

    @classmethod
    def make_task_args(cls, args: CommandLineArguments) -> Literal[None]:
        if not args.get_bool(cls.cli_flag()):
            raise CannotMakeArguments()
