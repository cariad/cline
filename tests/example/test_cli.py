from typing import List, Type

from pytest import mark

import cline.tasks
import example.tasks
from cline import AnyTask
from example.cli import ExampleCli


@mark.parametrize(
    "args, expect",
    [
        ([], cline.tasks.HelpTask),
        (["--version"], cline.tasks.HelpTask),
        (["1", "2", "--sub"], example.tasks.SubtractTask),
        (["1", "2", "--sum"], example.tasks.SumTask),
    ],
)
def test(args: List[str], expect: Type[AnyTask]) -> None:
    cli = ExampleCli(args=args)
    assert isinstance(cli.task, expect)
