from argparse import ArgumentParser

import examples.example01.tasks
from cline.cli import ArgumentParserCli, RegisteredTasks


class ExampleCli(ArgumentParserCli):
    def make_parser(self) -> ArgumentParser:
        parser = ArgumentParser()
        parser.add_argument("a", help="first number", nargs="?")
        parser.add_argument("b", help="second number", nargs="?")
        return parser

    def register_tasks(self) -> RegisteredTasks:
        return [
            examples.example01.tasks.SumTask,
        ]
