from example import __version__
from example.cli import ExampleCli


def entry() -> None:
    ExampleCli.invoke_and_exit(app_version=__version__)


if __name__ == "__main__":
    entry()
