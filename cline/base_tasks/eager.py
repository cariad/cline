from typing import Literal

from cline.base_tasks.task import Task
from cline.command_line_arguments import CommandLineArguments


class EagerTask(Task[Literal[None]]):
    @classmethod
    def make_task_args(cls, args: CommandLineArguments) -> Literal[None]:
        return None
