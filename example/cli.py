from argparse import ArgumentParser
from typing import List

import example.tasks
from cline import AnyTaskType, Cli


class ExampleCli(Cli):
    @property
    def parser(self) -> ArgumentParser:
        parser = ArgumentParser()
        parser.add_argument("a", help="first number", nargs="?")
        parser.add_argument("b", help="second number", nargs="?")
        parser.add_argument("--sub", help="subtracts numbers", action="store_true")
        parser.add_argument("--sum", help="sums numbers", action="store_true")
        parser.add_argument("--version", help="show version", action="store_true")
        return parser

    @property
    def tasks(self) -> List[AnyTaskType]:
        return [
            example.tasks.SubtractTask,
            example.tasks.SumTask,
        ]
