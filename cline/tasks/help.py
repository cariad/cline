from dataclasses import dataclass

from cline.command_line_arguments import CommandLineArgs
from cline.exceptions import UserNeedsHelp
from cline.tasks.task import Task


@dataclass
class HelpArgs:
    explicit: bool


class HelpTask(Task[HelpArgs]):
    def invoke(self) -> int:
        raise UserNeedsHelp(explicit=self.args.explicit)

    @classmethod
    def make_args(cls, args: CommandLineArgs) -> HelpArgs:
        # We need to know if the user explicitly requested help or this is a
        # fallback position so we can return an appropriate shell exit code.
        return HelpArgs(
            explicit=args.get_bool("help", default=False),
        )
