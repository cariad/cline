from cline import CommandLineArgs, Task
from example.arguments import NumberArgs


class SubtractTask(Task[NumberArgs]):
    @classmethod
    def make_args(cls, args: CommandLineArgs) -> NumberArgs:
        """
        Creates arguments for this task based on the command line `args`.
        """

        # Assert that the "sub" flag is truthy:
        args.assert_true("sub")

        # If "a" or "b" aren't set or aren't integers then "get_integer" will raise
        # CannotMakeArguments:
        return NumberArgs(
            a=args.get_integer("a"),
            b=args.get_integer("b"),
        )

    def invoke(self) -> int:
        """
        Invokes this task.

        Returns the shell exit code.
        """

        sum = self.args.a - self.args.b
        self.out.write(str(sum) + "\n")
        return 0
