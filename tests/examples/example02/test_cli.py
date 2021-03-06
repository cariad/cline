from typing import List, Type

from pytest import mark

import cline.tasks
import examples.example02.tasks
from cline import AnyTask
from examples.example02.cli import ExampleCli


@mark.parametrize(
    "args, expect",
    [
        ([], cline.tasks.HelpTask),
        (["--version"], cline.tasks.HelpTask),
        (["1", "2", "--sub"], examples.example02.tasks.SubtractTask),
        (["1", "2", "--sum"], examples.example02.tasks.SumTask),
    ],
)
def test(args: List[str], expect: Type[AnyTask]) -> None:
    cli = ExampleCli(args=args)
    assert isinstance(cli.task, expect)
