import importlib.resources as pkg_resources

from cline.base_tasks import EagerTask, FlagTask, Task
from cline.cli import AnyTask, Cli
from cline.command_line_arguments import CommandLineArguments
from cline.exceptions import CannotMakeArguments, CommandLineArgumentError

with pkg_resources.open_text(__package__, "VERSION") as t:
    __version__ = t.readline().strip()

__all__ = [
    "AnyTask",
    "CannotMakeArguments",
    "Cli",
    "CommandLineArguments",
    "CommandLineArgumentError",
    "FlagTask",
    "Task",
    "EagerTask",
]
