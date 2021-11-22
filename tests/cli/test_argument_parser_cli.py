from argparse import ArgumentParser
from io import StringIO

from cline.cli import ArgumentParserCli, RegisteredTasks


class FooCli(ArgumentParserCli):
    def make_parser(self) -> ArgumentParser:
        parser = ArgumentParser()
        parser.add_argument("foo", help="bar")
        return parser

    def register_tasks(self) -> RegisteredTasks:
        return []


def test_write_help() -> None:
    out = StringIO()
    cli = FooCli(out=out)
    cli.write_help()
    assert "foo         bar" in out.getvalue()
