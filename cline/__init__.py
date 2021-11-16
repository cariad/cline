import importlib.resources as pkg_resources

from cline.cli import (
    AnyTask,
    CannotMakeArguments,
    Cli,
    CommandLineArgumentError,
    CommandLineArguments,
    EagerTask,
    FlagTask,
    Task,
)

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
