from dataclasses import dataclass
from typing import IO, Callable, Optional


@dataclass
class CliTaskConfig:
    exception_exit_code: int
    out: IO[str]
    render_help: Callable[[], None]
    version: Optional[str]
