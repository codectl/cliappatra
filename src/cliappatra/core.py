import argparse
import functools
import inspect
from typing import Any, Callable, Optional, Sequence

from cliappatra import utils
from cliappatra.actions import SubParsersAction
from cliappatra.models import Field
from cliappatra.parsers import FieldParser


class ArgumentParser(argparse.ArgumentParser):
    ACTIONS = "Actions"
    ARGUMENTS = "Arguments"
    OPTIONS = "Options"
    HELP = "Help"

    def __init__(
            self,
            prog: Optional[str] = None,
            description: Optional[str] = None,
            version: Optional[str] = None,
            epilog: Optional[str] = None,
            add_help: bool = True,
            callback: Callable[..., Any] = None,
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
        self._arguments = add_group(ArgumentParser.ARGUMENTS)
        self._options = add_group(ArgumentParser.OPTIONS)
        self._help = add_group(ArgumentParser.HELP)

        self.add_help = add_help
        self.version = version

        self._parsed: (ArgumentParser, argparse.Namespace) = None
        if callback is not None:
            self._fields = None
            self._callback = callback
            self.init_parser(callback)

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

    def init_parser(self, fn: Callable[..., Any]):
        self._fields = self._add_fields(fn=fn)
        if hasattr(fn, "subactions"):
            self.register_subactions(fn.subactions)

    def parse_args(self, args=None, namespace=None):
        namespace = super().parse_args(args=args, namespace=namespace)
        self.invoke_callbacks(namespace)

    def invoke_callbacks(self, namespace):
        args, kwargs = utils.fields_to_params(namespace=namespace, fields=self._fields)
        self._callback(*args, **kwargs)
        if self._parsed:
            parser, subnamespace = self._parsed
            parser.invoke_callbacks(subnamespace)

    def register_subactions(self, callbacks: Sequence[Callable[..., Any]]):
        if not callbacks:
            return None

        subparsers = self.add_subparsers(
            title=ArgumentParser.ACTIONS,
            action=SubParsersAction,
            help="available actions",
        )

        for callback in callbacks:
            subparsers.add_parser("", callback=callback)

    def _add_fields(self, fn: Callable[..., Any]):
        fields = utils.get_func_fields(fn)
        for field in fields.values():
            self._add_field(field)
        return fields

    def _add_field(self, field: Field):
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
    return ArgumentParser(
        prog=prog,
        description=description,
        epilog=epilog,
        callback=callback,
        **kwargs
    )


def subactions(*actions_args):
    def decorator(fn):
        fn.subactions = actions_args

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapper

    return decorator
