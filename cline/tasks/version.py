from cline.command_line_arguments import CommandLineArgs
from cline.exceptions import UserNeedsVersion
from cline.tasks.task import Task


class VersionTask(Task[None]):
    def invoke(self) -> int:
        raise UserNeedsVersion()

    @classmethod
    def make_args(cls, args: CommandLineArgs) -> None:
        args.assert_true("version")
