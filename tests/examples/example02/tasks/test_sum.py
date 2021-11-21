from io import StringIO

from cline import CommandLineArguments
from examples.example02.arguments import NumberArgs
from examples.example02.tasks import SumTask


def test_make_args() -> None:
    cli_args = CommandLineArguments(
        {
            "a": "1",
            "b": "2",
            "sum": True,
        }
    )

    args = SumTask.make_args(cli_args)
    assert args == NumberArgs(a=1, b=2)


def test_invoke() -> None:
    out = StringIO()
    task = SumTask(args=NumberArgs(a=5, b=2), out=out)
    assert task.invoke() == 0
    assert out.getvalue() == "7\n"
