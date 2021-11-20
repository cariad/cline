from importlib.resources import open_text

from cline.cli import Cli
from cline.command_line_arguments import CommandLineArgs
from cline.exceptions import CannotMakeArguments
from cline.tasks import AnyTask, AnyTaskType, Task

with open_text(__package__, "VERSION") as t:
    __version__ = t.readline().strip()

__all__ = [
    "AnyTask",
    "AnyTaskType",
    "Cli",
    "CommandLineArgs",
    "CannotMakeArguments",
    "Task",
]
