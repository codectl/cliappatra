import argparse
import inspect
from dataclasses import is_dataclass
from typing import Any, Callable, Optional

from cliappatra import utils
from cliappatra.models import Field, FieldMeta


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
            exit_on_error=True,
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

    def _parse_field(self, field: Field):

        kwargs = field.asdict()
        meta = kwargs.pop("meta")

        if "action" not in kwargs:
            kwargs["action"] = self._annotation_action(meta.annotation)

        if meta.kind == inspect.Parameter.POSITIONAL_ONLY:
            group = self._arguments
            name = meta.name
            required = kwargs.pop("required")

            if "nargs" not in kwargs and not required:
                kwargs["nargs"] = "?"

            if "metavar" not in kwargs:
                kwargs["metavar"] = name.upper()

        else:
            group = self._options
            name = f"--{meta.name}"

        # required = kwargs.pop("required")
        # env = kwargs.pop("envar")

        return group.add_argument(name, **kwargs)

    @staticmethod
    def _annotation_action(annotation):
        if annotation is bool:
            return "store_true"
        return "store"


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
