class ClineError(Exception):
    pass


class CannotMakeArguments(ClineError):
    pass


class NoAvailableTasks(ClineError):
    pass


class CommandLineArgumentError(ClineError):
    pass


class MissingArgumentError(CommandLineArgumentError):
    pass


class UnexpectedArgumentTypeError(CommandLineArgumentError):
    pass
