from typing import List, Union

from pytest import mark, raises

from cline import CommandLineArguments
from cline.exceptions import CannotMakeArguments


@mark.parametrize("value", ["bar", ["woo", "bar"]])
def test_assert_string_ok(value: Union[List[str], str]) -> None:
    args = CommandLineArguments(
        {
            "foo": "bar",
        }
    )
    args.assert_string(arg="foo", value=value)
    assert True


@mark.parametrize("value", ["woo", ["woo", "boo"]])
def test_assert_string__fail(value: Union[List[str], str]) -> None:
    args = CommandLineArguments(
        {
            "foo": "bar",
        }
    )
    with raises(CannotMakeArguments):
        args.assert_string(arg="foo", value=value)


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


def test_get_string__default() -> None:
    args = CommandLineArguments()
    assert args.get_string("foo", "bar") == "bar"


def test_get_string__none() -> None:
    args = CommandLineArguments()
    with raises(CannotMakeArguments):
        args.get_string("foo")
