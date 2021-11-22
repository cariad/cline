from io import StringIO
from logging import NOTSET, WARNING, getLogger
from typing import List

from mock import patch

from cline import CommandLineArguments
from cline.cli import Cli, RegisteredTasks
from cline.tasks import HelpTask, Task, VersionTask


class RaiseKeyboardInterruptTask(Task[bool]):
    @classmethod
    def make_args(cls, args: CommandLineArguments) -> bool:
        args.assert_true("keyboard_interrupt")
        return True

    def invoke(self) -> int:
        raise KeyboardInterrupt()


class RaiseValueErrorTask(Task[bool]):
    @classmethod
    def make_args(cls, args: CommandLineArguments) -> bool:
        args.assert_true("value_error")
        return True

    def invoke(self) -> int:
        raise ValueError("this is a value error")


class FooParser:
    pass


class FooCli(Cli[FooParser]):
    def register_tasks(self) -> RegisteredTasks:
        return [
            RaiseKeyboardInterruptTask,
            RaiseValueErrorTask,
        ]

    def make_cli_args(self, args: List[str]) -> CommandLineArguments:
        return CommandLineArguments(
            {
                "keyboard_interrupt": "--keyboard-interrupt" in args,
                "help": "--help" in args,
                "value_error": "--value-error" in args,
                "version": "--version" in args,
            }
        )

    def make_parser(self) -> FooParser:
        return FooParser()

    def write_help(self) -> None:
        self.out.write("help\n")


def test_app_version() -> None:
    cli = FooCli(app_version="1.0.1")
    assert cli.app_version == "1.0.1"


def test_parser__make_once() -> None:
    cli = FooCli()
    assert cli.parser is cli.parser


def test_task__falls_back_to_version() -> None:
    cli = FooCli(app_version="1.0.0", args=["--version"])
    assert isinstance(cli.task, VersionTask)


def test_task__falls_back_to_help_when_no_app_version() -> None:
    cli = FooCli(args=["--version"])
    assert isinstance(cli.task, HelpTask)


def test_task__falls_back_to_help_when_no_version_flag() -> None:
    cli = FooCli(app_version="1.0.0")
    assert isinstance(cli.task, HelpTask)


def test_invoke_and_exit__with_init_logging() -> None:
    result = {"exit_code": -1}

    def done(exit_code: int) -> None:
        result["exit_code"] = exit_code

    with patch("cline.cli.cli.basicConfig") as basic_config:
        FooCli.invoke_and_exit(args=["--help"], callback=done)

    basic_config.assert_called_once_with(
        format="%(levelname)s • %(name)s • %(pathname)s:%(lineno)d • %(message)s"
    )
    assert result["exit_code"] == 0


def test_invoke_and_exit__no_init_logging() -> None:
    result = {"exit_code": -1}

    def done(exit_code: int) -> None:
        result["exit_code"] = exit_code

    with patch("cline.cli.cli.basicConfig") as basic_config:
        FooCli.invoke_and_exit(args=["--help"], callback=done, init_logging=False)

    basic_config.assert_not_called()
    assert result["exit_code"] == 0


def test_invoke_and_exit__no_log_level() -> None:
    result = {"exit_code": -1}

    def done(exit_code: int) -> None:
        result["exit_code"] = exit_code

    FooCli.invoke_and_exit(args=["--help"], callback=done)

    assert getLogger("cline").level == NOTSET
    assert result["exit_code"] == 0


def test_invoke_and_exit__with_log_level() -> None:
    result = {"exit_code": -1}

    def done(exit_code: int) -> None:
        result["exit_code"] = exit_code

    FooCli.invoke_and_exit(args=["--help"], callback=done, log_level="WARNING")

    assert getLogger("cline").level == WARNING
    assert result["exit_code"] == 0


def test_invoke_and_exit__explicit_help() -> None:
    result = {"exit_code": -1}

    def done(exit_code: int) -> None:
        result["exit_code"] = exit_code

    out = StringIO()
    FooCli.invoke_and_exit(
        args=["--help"],
        callback=done,
        log_level="WARNING",
        out=out,
    )
    assert out.getvalue() == "help\n"
    assert result["exit_code"] == 0


def test_invoke_and_exit__implicit_help() -> None:
    result = {"exit_code": -1}

    def done(exit_code: int) -> None:
        result["exit_code"] = exit_code

    out = StringIO()
    FooCli.invoke_and_exit(
        args=[],
        callback=done,
        log_level="WARNING",
        out=out,
    )
    assert out.getvalue() == "help\n"
    assert result["exit_code"] == 1


def test_invoke_and_exit__keyboard_interrupt() -> None:
    result = {"exit_code": -1}

    def done(exit_code: int) -> None:
        result["exit_code"] = exit_code

    FooCli.invoke_and_exit(
        args=["--keyboard-interrupt"],
        callback=done,
    )
    assert result["exit_code"] == 100


def test_invoke_and_exit__value_error() -> None:
    result = {"exit_code": -1}

    def done(exit_code: int) -> None:
        result["exit_code"] = exit_code

    out = StringIO()

    FooCli.invoke_and_exit(
        args=["--value-error"],
        callback=done,
        out=out,
    )

    assert out.getvalue() == "🔥 this is a value error\n"
    assert result["exit_code"] == 101


def test_invoke_and_exit__version() -> None:
    result = {"exit_code": -1}

    def done(exit_code: int) -> None:
        result["exit_code"] = exit_code

    out = StringIO()
    FooCli.invoke_and_exit(
        app_version="1.1.1",
        args=["--version"],
        callback=done,
        out=out,
    )
    assert out.getvalue() == "1.1.1\n"
    assert result["exit_code"] == 0
