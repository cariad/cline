from examples.full import __version__
from examples.full.cli import ExampleCli


def entry() -> None:
    ExampleCli.invoke_and_exit(app_version=__version__)


if __name__ == "__main__":
    entry()
