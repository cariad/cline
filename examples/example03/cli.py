from argparse import ArgumentParser

import examples.example03.tasks
from cline.cli import ArgumentParserCli, RegisteredTasks


class ExampleCli(ArgumentParserCli):
    def make_parser(self) -> ArgumentParser:
        parser = ArgumentParser()
        parser.add_argument("a", help="first number", nargs="?")
        parser.add_argument("b", help="second number", nargs="?")
        parser.add_argument("--sub", help="subtracts numbers", action="store_true")
        parser.add_argument("--sum", help="sums numbers", action="store_true")
        parser.add_argument("--version", help="show version", action="store_true")
        return parser

    def register_tasks(self) -> RegisteredTasks:
        return [
            examples.example03.tasks.SubtractTask,
            examples.example03.tasks.SumTask,
        ]
