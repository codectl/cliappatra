import argparse
import inspect
from dataclasses import asdict, is_dataclass
from typing import Any, Callable, Optional, Sequence, Union

from pydantic import BaseModel

from cliappatra import utils
from cliappatra.models import Field, ParamMeta


class ArgumentParser(argparse.ArgumentParser):

    def __init__(
            self,
            prog: Optional[str] = None,
            description: Optional[str] = None,
            version: Optional[str] = None,
            epilog: Optional[str] = None,
            add_help: bool = True,
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
        self._arguments = add_group("Arguments")
        self._options = add_group("Options")
        self._help = add_group("Help")

        # print(self._action_groups)

        self.add_help = add_help
        self.version = version

        if add_help:
            self._help.add_argument(
                "-h",
                "--help",
                action="help",
                default=argparse.SUPPRESS,
                help="show this help message and exit",
            )

        if version:
            self._help.add_argument(
                "-v",
                "--version",
                action="version",
                default=argparse.SUPPRESS,
                help="show program's version number and exit",
            )

    def parse_function(self, parser: Callable[..., Any]):
        params = utils.get_func_params(parser)
        for param in params.values():
            self._parse_field(param)

    def _parse_field(self, param: ParamMeta):

        kwargs = {}
        if is_dataclass(param.default):
            kwargs.update(param.default.asdict())

        if param.kind == inspect.Parameter.POSITIONAL_ONLY:
            group = self._arguments
            name = param.name
            if not kwargs.get("metavar"):
                kwargs["metavar"] = name.upper()
        else:
            group = self._options
            name = f"--{param.name}"

        # required = kwargs.pop("required")
        if not kwargs.get("action"):
            kwargs["action"] = self._annotation_action(param.annotation)
        # env = kwargs.pop("envar")

        return group.add_argument(name, **kwargs)

    @staticmethod
    def _annotation_action(annotation):
        if annotation is bool:
            return argparse.BooleanOptionalAction
        return argparse.Action


def create_app(
        prog: Optional[str] = None,
        description: Optional[str] = None,
        epilog: Optional[str] = None,
        parser: Optional[Callable[..., Any]] = None,
        **kwargs
) -> ArgumentParser:
    app = ArgumentParser(
        prog=prog,
        description=description,
        epilog=epilog,
        **kwargs
    )

    if parser is not None:
        app.parse_function(parser)

    return app
