import argparse
import inspect
from typing import Any, Callable, Optional

from cliappatra import utils
from cliappatra.models import Field
from cliappatra.parsers import FieldParser


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
        self._subcommands = ()
        self._arguments = add_group("Arguments")
        self._options = add_group("Options")
        self._help = add_group("Help")
        self._callback = None

        # print(self._action_groups)

        self.add_help = add_help
        self.version = version

        if add_help:
            self._help.add_argument(
                "-h",
                "--help",
                action="help",
                dest=argparse.SUPPRESS,
                help="show this help message and exit",
            )

        if version:
            self._help.add_argument(
                "-v",
                "--version",
                action="version",
                dest=argparse.SUPPRESS,
                help="show program's version number and exit",
            )

    def _commands(self):
        if not self._subcommands:
            # Add Sub-Commands Group
            # self._subcommands = self.add_subparsers(
            #     title=ArgumentParser.COMMANDS,
            #     action=argparse.SubParsersAction,
            #     required=True,
            # )

            # Shuffle Group to the Top for Help Message
            self._action_groups.insert(0, self._action_groups.pop())

        # Return
        return self._subcommands

    def parse_args(self, args=None, namespace=None):
        namespace = super().parse_args(args=args, namespace=namespace)
        args, kwargs = utils.fields_to_params(namespace=namespace, fields=self._callback.fields)
        self._callback(*args, **kwargs)

    def callback(self, fn: Callable[..., Any]):
        fn.fields = self._parse_callback(fn=fn)
        self._callback = fn

    def _parse_callback(self, fn: Callable[..., Any]):
        fields = utils.get_func_fields(fn)
        for field in fields.values():
            self._parse_field(field)
        return fields

    def _parse_field(self, field: Field):
        args, kwargs = FieldParser.parse(field)
        group = self._arguments if field.meta.kind == inspect.Parameter.POSITIONAL_ONLY else self._options
        group.add_argument(*args, **kwargs)


def create_app(
        prog: Optional[str] = None,
        description: Optional[str] = None,
        epilog: Optional[str] = None,
        callback: Optional[Callable[..., Any]] = None,
        **kwargs
) -> ArgumentParser:
    app = ArgumentParser(
        prog=prog,
        description=description,
        epilog=epilog,
        **kwargs
    )

    if callback is not None:
        app.callback(callback)

    return app
