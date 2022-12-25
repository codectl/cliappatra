import argparse
from typing import Any, Callable, Optional, Sequence, Union

from pydantic import BaseModel


class Arg(BaseModel):
    name: Union[str, Sequence[str]]
    action: argparse.Action
    nargs: Union[int, str]
    const: Optional[str]
    default: Optional[Any]
    required: bool
    help: Optional[str]
    metavar: Optional[str]
    dest: Optional[str]


class Cliappatra(argparse.ArgumentParser):

    def __init__(
            self,
            prog: Optional[str] = None,
            description: Optional[str] = None,
            version: Optional[str] = None,
            epilog: Optional[str] = None,
            add_help: bool = True,
            commands=(),
            **kwargs
    ):
        super().__init__(
            prog=prog,
            description=description,
            epilog=epilog,
            add_help=False,
            **kwargs
        )

        add_group = self.add_argument_group
        self._positionals = add_group("Arguments")
        self._optionals = add_group("Options")
        self._help = add_group("Help")

        print(self._action_groups)

        self.add_help = add_help
        self.version = version

        if self.add_help:
            self._add_help_opt()
        if self.version:
            self._add_version_opt()

    def _add_version_opt(self) -> None:
        self._help.add_argument(
            "-v",
            "--version",
            action="version",
            help="show program's version number and exit",
        )

    def _add_help_opt(self) -> None:
        self._help.add_argument(
            "-h",
            "--help",
            action="help",
            help="show this help message and exit",
        )


def create_app(function: Callable[..., Any]) -> None:
    app = Cliappatra()
    app.command()(function)
    app()
