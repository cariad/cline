from cline import CommandLineArguments, Task
from examples.example02.arguments import NumberArgs


class SubtractTask(Task[NumberArgs]):
    @classmethod
    def make_args(cls, args: CommandLineArguments) -> NumberArgs:
        """
        Makes and returns strongly-typed arguments for this task based on the
        parsed command line arguments `args`.

        Arguments:
            args: Parsed command line arguments

        Raises:
            CannotMakeArguments: If the given arguments are not relevant to this
            task

        Returns:
            Task arguments
        """

        # Asserts that the "sub" flag is present and truthy.
        args.assert_true("sub")

        # If "a" or "b" aren't set or aren't integers then "get_integer" will
        # raise `CannotMakeArguments`:
        return NumberArgs(
            a=args.get_integer("a"),
            b=args.get_integer("b"),
        )

    def invoke(self) -> int:
        """
        Invokes the task.

        Reads arguments from `self.args`. Writes output to `self.out`.

        Returns the shell exit code.
        """

        # Since the arguments are strongly-typed, we don't need to worry about
        # parsing integers and handing failures therein:
        result = self.args.a - self.args.b
        self.out.write(f"{result}\n")
        return 0
