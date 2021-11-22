from pytest import raises

from cline import CommandLineArguments
from cline.exceptions import CannotMakeArguments


def test_get_bool__none_with_no_default() -> None:
    args = CommandLineArguments()
    with raises(CannotMakeArguments):
        args.get_bool("foo")


def test_get_integer__not_parseable() -> None:
    args = CommandLineArguments(
        {
            "foo": "bar",
        }
    )
    with raises(CannotMakeArguments):
        args.get_integer("foo")


def test_get_string_none() -> None:
    args = CommandLineArguments()
    with raises(CannotMakeArguments):
        args.get_string("foo")
