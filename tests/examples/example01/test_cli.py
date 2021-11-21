from typing import List, Type

from pytest import mark

from cline import AnyTask
from examples.example01.cli import ExampleCli
from examples.example01.tasks import NumberArgs, SumTask


@mark.parametrize(
    "args, expect_task, expect_args",
    [
        (["1", "2"], SumTask, NumberArgs(a=1, b=2)),
    ],
)
def test(
    args: List[str],
    expect_task: Type[AnyTask],
    expect_args: NumberArgs,
) -> None:
    cli = ExampleCli(args=args)
    assert isinstance(cli.task, expect_task)
    assert cli.task.args == expect_args
