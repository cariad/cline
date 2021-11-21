# 📜 Cline

**Cline** is a Python package that helps you build command line applications.

**Cline** separates the two concerns of "understanding the command line arguments you receive" and "operating on strongly-typed arguments" and helps you to write clean, testable tasks.

<edition value="toc" />

## Examples

### Example 1: Summing two integers

_The source code for this example is available at [github.com/cariad/cline/blob/main/examples/sum](https://github.com/cariad/cline/blob/main/examples/sum). The tests are in [github.com/cariad/cline/blob/main/tests/examples/sum](https://github.com/cariad/cline/blob/main/tests/examples/sum)._

In this example, we'll build an application that sums two integers on the command line then prints the result:

```bash
python -m examples.sum 1 3
```

<!--edition-exec as=markdown fence=backticks host=shell range=start-->

```text
4
```

<!--edition-exec range=end-->

#### 1. Create a CLI class with an argument parser

For this example, we'll parse the command line arguments with Python's baked-in `ArgumentParser`. Cline provides an `ArgumentParserCli` base class for this.

Create a class named `ExampleCli` that inherits from `cline.cli.ArgumentParserCli`. Override `make_parser()` to return an `ArgumentParser` that accepts two numbers.

For example:

```python
from argparse import ArgumentParser
from cline.cli import ArgumentParserCli

class ExampleCli(ArgumentParserCli):
    def make_parser(self) -> ArgumentParser:
        parser = ArgumentParser()
        parser.add_argument(
          "a",
          help="first number",
          nargs="?",
        )
        parser.add_argument(
          "b",
          help="second number",
          nargs="?",
        )
        return parser
```

#### 2. Creating a task

A task does two things:

1. Converts the command line arguments to strongly-typed task arguments
1. Operates on strongly-typed task arguments

We'll start with the strongly-typed task arguments. Since we'll be summing two integers, let's define a dataclass that holds two integers:

```python
from dataclasses import dataclass

@dataclass
class NumberArgs:
    a: int
    b: int
```

Now we need a way to convert command line arguments to these task arguments. Create a class named `SumTask` and inherit from `cline.Task`. `Task` is generic and requires your strongly-typed arguments type.

```python
from dataclasses import dataclass
from cline import CommandLineArguments, Task

@dataclass
class NumberArgs:
    a: int
    b: int

class SumTask(Task[NumberArgs]):
    pass
```

To convert command line arguments to strongly-typed task arguments, override the `make_args()` method:

```python
from dataclasses import dataclass
from cline import CommandLineArguments, Task

@dataclass
class NumberArgs:
    a: int
    b: int

class SumTask(Task[NumberArgs]):
    @classmethod
    def make_args(cls, args: CommandLineArguments) -> NumberArgs:
        return NumberArgs(
            a=args.get_integer("a"),
            b=args.get_integer("b"),
        )
```

`CommandLineArguments` wraps the parsed command line arguments with some handy functions for reading argument values.

For example, since we named the two numbers `a` and `b` in the parser earlier, we can refer to them by name and call `get_integer()` to get their values.

Note that `CommandLineArguments` will raise `CannotMakeArguments` if `a` or `b` aren't set or can't be parsed as integers. This is the correct way to indicate that task arguments cannot be made for a given task. You don't need to validate the arguments yourself.

Now that `SumTask` knows how to create strongly-typed arguments, we can operate on them.

Override the `invoke()` method to:

1. Operate on `self.args`
1. Write output to `self.out`
1. Return the shell exit code

In this example, `invoke()` sums the two integer arguments, writes the result, then returns `0` to indicate success:

```python
from dataclasses import dataclass
from cline import CommandLineArguments, Task

@dataclass
class NumberArgs:
    a: int
    b: int

class SumTask(Task[NumberArgs]):
    @classmethod
    def make_args(cls, args: CommandLineArguments) -> NumberArgs:
        return NumberArgs(
            a=args.get_integer("a"),
            b=args.get_integer("b"),
        )

    def invoke(self) -> int:
        result = self.args.a + self.args.b
        self.out.write(f"{result}\n")
        return 0
```

#### 3. Registering the task with the CLI

Back in your CLI class, override `register_tasks()` to register `SumTask`:

```python
from argparse import ArgumentParser
from cline.cli import ArgumentParserCli
from examples.sum.sum import SumTask

class ExampleCli(ArgumentParserCli):
    def make_parser(self) -> ArgumentParser:
        parser = ArgumentParser()
        parser.add_argument(
          "a",
          help="first number",
          nargs="?",
        )
        parser.add_argument(
          "b",
          help="second number",
          nargs="?",
        )
        return parser

    def register_tasks(self) -> RegisteredTasks:
        return [
            SumTask,
        ]
```

#### 4. Creating a CLI entry point

Finally, create a `__main__.py` script that calls your CLI's `invoke_and_exit()` method:

```python
from examples.sum.cli import ExampleCli

def entry() -> None:
    ExampleCli.invoke_and_exit()

if __name__ == "__main__":
    entry()
```

And that's it! You can now sum integers on the command line:

```bash
python -m examples.sum 1 3
```

<!--edition-exec as=markdown fence=backticks host=shell range=start-->

```text
4
```

<!--edition-exec range=end-->

#### 4. Unit testing

Cline was designed to support easy high coverage of your work.

To test your task's `make_args()` function, construct your own `CommandLineArguments` instance with the command line arguments to test, then verify that `make_args()` returns the strongly-typed arguments that you'd expect:

```python
from cline import CommandLineArguments
from examples.sum.sum import SumTask, NumberArgs

def test_make_args() -> None:
    cli_args = CommandLineArguments(
        {
            "a": "1",
            "b": "2",
        }
    )

    args = SumTask.make_args(cli_args)
    assert args == NumberArgs(a=1, b=2)
```

To test your task's `invoke()` function, construct your own strongly-typed arguments and an output writer then assert that the shell exit code and written response are as you expect:

```python
from io import StringIO
from examples.sum.sum import SumTask, NumberArgs

def test_invoke() -> None:
    out = StringIO()
    task = SumTask(args=NumberArgs(a=5, b=2), out=out)
    assert task.invoke() == 0
    assert out.getvalue() == "7\n"
```

To test that the CLI will invoke your task for a given set of command line arguments, you can instantiate your CLI with the arguments to test then assert that the `.task` and `.task.args` properties are as you expect:

```python
from typing import List, Type

from pytest import mark

from cline import AnyTask
from examples.sum.cli import ExampleCli
from examples.sum.tasks.sum import NumberArgs, SumTask

@mark.parametrize(
    "args, expect_task, expect_args",
    [
        (["1", "2"], SumTask, NumberArgs(a=1, b=2)),
    ],
)
def test(
    args: List[str],
    expect_task: Type[AnyTask],
    expect_args: NumberArgs,
) -> None:
    cli = ExampleCli(args=args)
    assert isinstance(cli.task, expect_task)
    assert cli.task.args == expect_args
```

### Example 2: Adding support for subtraction

_The source code for this example is available at [github.com/cariad/cline/blob/main/examples/subtract](https://github.com/cariad/cline/blob/main/examples/subtract). The tests are in [github.com/cariad/cline/blob/main/tests/examples/subtract](https://github.com/cariad/cline/blob/main/tests/examples/subtract)._

In this example, we'll build on Example 1 to allow integers to be subtracted. We'll add `--sum` and `--sub` flags to describe that we want to do.

For example:

```bash
python -m examples.subtract --sum 8 5
python -m examples.subtract --sub 8 5
```

<!--edition-exec as=markdown fence=backticks host=shell range=start-->

```text
13
3
```

<!--edition-exec range=end-->

#### 1. Add the new flags to the argument parser

In your CLI class, update the argument parser to support `--sum` and `--sub` flags:

```python
def make_parser(self) -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("a", help="first number", nargs="?")
    parser.add_argument("b", help="second number", nargs="?")
    parser.add_argument("--sub", help="subtracts", action="store_true")
    parser.add_argument("--sum", help="sums", action="store_true")
    return parser
```

Note that the new arguments are presented as `--sub` and `--sum` here, but their names omit the dashes. The new arguments are named `sub` and `sum`.

#### 2. Update SumTask to require the "--sum" flag

In the previous example, we wanted `SumTask` to always run if we gave it two numbers. Now we want it to run only if we give it two numbers _and_ the `--sum` flag.

We can achieve this simply by calling `assert_true()` with the name of the flag we want to assert is truthy:

```python
@classmethod
def make_args(cls, args: CommandLineArguments) -> NumberArgs:
    args.assert_true("sum")

    return NumberArgs(
        a=args.get_integer("a"),
        b=args.get_integer("b"),
    )
```

#### 3. Create the SubtractTask class

To perform subtraction, we'll need a `SubtractTask` class. This is almost identical to `SumTask`, expect:

1. We want to assert that the `sub` (not `sum`) flag is truthy
1. We want to subtract (not sum) the arguments

So, for example:

```python
class SubtractTask(Task[NumberArgs]):
    @classmethod
    def make_args(cls, args: CommandLineArguments) -> NumberArgs:
        args.assert_true("sub")

        return NumberArgs(
            a=args.get_integer("a"),
            b=args.get_integer("b"),
        )

    def invoke(self) -> int:
        result = self.args.a - self.args.b
        self.out.write(f"{result}\n")
        return 0
```

#### 4. Register the SubtractTask class

Open your CLI class and register `SubtractTask`:

```python
def register_tasks(self) -> RegisteredTasks:
    return [
        examples.full.tasks.SubtractTask,
        examples.full.tasks.SumTask,
    ]
```

...and that's it! When your application runs, Cline will try each registered task in order until one is found that accepts the given command line arguments, then executes it:

```bash
python -m examples.subtract --sum 8 5
python -m examples.subtract --sub 8 5
```

<!--edition-exec as=markdown fence=backticks host=shell range=start-->

```text
13
3
```

<!--edition-exec range=end-->

### Example 3: Supporting help and versions

_The source code for this example is available at [github.com/cariad/cline/blob/main/examples/full](https://github.com/cariad/cline/blob/main/examples/full). The tests are in [github.com/cariad/cline/blob/main/tests/examples/full](https://github.com/cariad/cline/blob/main/tests/examples/full)._

Cline has baked-in support for printing your application's help and version on the command line.

Enabling support for help is easy enough: it's already enabled. If Cline cannot find any registered tasks that can handle the given command line arguments then it will print the argument parser's help.

For example, if we run one of the above examples without specifying any numbers then each task's `make_args()` call will fail and Cline will fall back to displaying the help:

```bash
python -m examples.sum
```

<!--edition-exec as=markdown fence=backticks host=shell range=start-->

```text
usage: __main__.py [-h] [a] [b]

positional arguments:
  a           first number
  b           second number

options:
  -h, --help  show this help message and exit
```

<!--edition-exec range=end-->

Adding support for version printing is a two-step process. First, add a `--version` flag to your argument parser:

```python
def make_parser(self) -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("a", help="first number", nargs="?")
    parser.add_argument("b", help="second number", nargs="?")
    parser.add_argument("--sub", help="subtracts numbers", action="store_true")
    parser.add_argument("--sum", help="sums numbers", action="store_true")
    parser.add_argument("--version", help="show version", action="store_true")
    return parser
```

Then in `__main__.py`, pass your application's version into `invoke_and_exit()`:

```python
from examples.full import __version__
from examples.full.cli import ExampleCli

def entry() -> None:
    ExampleCli.invoke_and_exit(app_version=__version__)

if __name__ == "__main__":
    entry()
```

Note that this depends on your own implementation of versioning. I use `__version__` but you don't have to. If your application's version is gettable via a property other than `__version__` then pass that instead.

```bash
python -m examples.full --version
```

<!--edition-exec as=markdown fence=backticks host=shell range=start-->

```text
1.2.3
```

<!--edition-exec range=end-->

### Example 4: Making your package executable after installing

This isn't Cline functionality, but I'll preempt the question by answering it now.

In your `setup.py` script, pass an `entry_points` value into `setup()`:

```python
setup(
    # ...
    entry_points={
        "console_scripts": [
            "foo=bar.__main__:entry",
        ],
    },
    # ...
)
```

Note that:

- `foo` is the name of the command you want your users to run (i.e. `foo --help`)
- `bar` is your package name
- `entry` is the name of the function to run inside `__main__.py`

## API reference

### `cline.cli.Cli[TParser]` abstract class

The `Cli` abstract class is the entry point and manager of the tasks invoked on behalf of the host application.

`Cli` isn't opinionated on how you choose to parse command line arguments. The `TParser` generic type describes whichever parser you choose. A `ArgumentParserCli` class is provided which uses Python's baked-in `argparse.ArgumentParser`.

### `cline.cli.ArgumentParserCli` abstract class

`ArgumentParserCli` is an implementation of `Cli` that uses Python's baked-in `argparse.ArgumentParser` to parse arguments.

The functions that must be overridden and implemented are:

- `make_parser()` must return an instance of `argparse.ArgumentParser` configured for your project.
- `register_tasks()` must return the ordered list of `Task` classes to be considered for invocation.

### `cline.Task[TTaskArgs]` abstract class

The `Task` abstract class represents a type of work that can be invoked via the command line.

`Task` separates the two concerns of:

1. Converting the user-entered command line arguments to strongly-typed arguments
1. Operating on strongly-typed arguments

The `TTaskArgs` generic type describes a task's strongly-typed arguments.

The functions that must be overridden and implemented are:

- `make_args(args: CommandLineArguments)` must interrogate the given command line arguments and return strongly-typed arguments. Raise `CannotMakeArguments` if the given command line arguments cannot be used to prepare this task.
- `invoke()` must perform the task's work then return the shell exit code.

The following properties are available during invocation:

- `self.args` gets the task's strongly-typed arguments.
- `self.out` gets the output writer.

### `cline.CommandLineArguments` class

A `CommandLineArguments` instance will be passed to `Task.make_args` to help you interpret the user-entered command line arguments.

- `assert_true(key: str)` asserts that the command line flag is truthy. Raises `CannotMakeArguments` if not.
- `get_bool(key: str, default: Optional[bool] = None)` gets the boolean value of the given argument. If the argument isn't set to a boolean value and a default value isn't specified then `CannotMakeArguments` is raised.
- `get_integer(key: str)` gets the integer value of the given argument. If the argument isn't set to a integer value then `CannotMakeArguments` is raised.
- `get_string(key: str)` gets the string value of the given argument. If the argument isn't set to a string value then `CannotMakeArguments` is raised.

## Acknowledgements

- This documentation was pressed with [Edition](https://cariad.github.io/edition/).
