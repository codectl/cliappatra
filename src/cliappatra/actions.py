"""Recursively Nesting Sub-Parsers Action for Typed Argument Parsing.

The `actions` module contains the `SubParsersAction` class, which is an action
that provides recursive namespace nesting when parsing sub-commands.
"""


import argparse
from gettext import gettext as _
from typing import Callable

from typing import Any, Optional, Sequence, Union, cast


# class SubParsersAction(argparse._SubParsersAction):
#
#     def __call__(
#         self,
#         parser: argparse.ArgumentParser,
#         namespace: argparse.Namespace,
#         values: Union[str, Sequence[Any], None],
#         option_string: Optional[str] = None,
#     ) -> None:
#
#         # Check values object is a sequence
#         # In order to not violate the Liskov Substitution Principle (LSP), the
#         # function signature for __call__ must match the base Action class. As
#         # such, this function signature also accepts "str" and "None" types for
#         # the value"s argument. However, in reality, this should only ever be a
#         # list of strings here, so we just do a type cast.
#         values = cast(list[str], values)
#
#         # Get Parser Name and Remaining Argument Strings
#         parser_name, *arg_strings = values
#
#         # Try select the parser
#         try:
#             # Select the parser
#             parser = self._name_parser_map[parser_name]
#
#         except KeyError as exc:
#             # Parser doesn"t exist, raise an exception
#             raise argparse.ArgumentError(
#                 self,
#                 f"unknown parser {parser_name} (choices: {", ".join(self._name_parser_map)})"
#             ) from exc
#
#         # Parse all the remaining options into a sub-namespace, then embed this
#         # sub-namespace into the parent namespace
#         print("***")
#         print(parser)
#         print(self._name_parser_map)
#         print("***")
#
#         subnamespace, arg_strings = parser.parse_known_args(arg_strings)
#         setattr(namespace, parser_name, subnamespace)
#
#         # Store any unrecognized options on the parent namespace, so that the
#         # top level parser can decide what to do with them
#         if arg_strings:
#             vars(namespace).setdefault(argparse._UNRECOGNIZED_ARGS_ATTR, [])
#             getattr(namespace, argparse._UNRECOGNIZED_ARGS_ATTR).extend(arg_strings)


class SubParsersAction(argparse.Action):
    _UNRECOGNIZED_ARGS_ATTR = "_unrecognized_args"

    class _ChoicesPseudoAction(argparse.Action):

        def __init__(self, name, aliases, help):
            metavar = dest = name
            if aliases:
                metavar += " (%s)" % ", ".join(aliases)
            super().__init__(option_strings=[], dest=dest, help=help, metavar=metavar)

    def __init__(self,
                 option_strings,
                 prog,
                 parser_class,
                 dest=argparse.SUPPRESS,
                 required=False,
                 help=None,
                 metavar=None):

        self._prog_prefix = prog
        self._parser_class = parser_class
        self._name_parser_map = {}
        self._choices_actions = []

        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=argparse.PARSER,
            choices=self._name_parser_map,
            required=required,
            help=help,
            metavar=metavar)

    def add_parser(self, name, **kwargs):
        callback = kwargs["callback"]
        name = name or callback.__name__
        if kwargs.get("prog") is None:
            kwargs["prog"] = f"{self._prog_prefix} {name}"

        aliases = kwargs.pop("aliases", ())

        # create a pseudo-action to hold the choice help
        help_ = kwargs.pop("help") if "help" in kwargs else callback.__doc__
        if help_:
            choice_action = self._ChoicesPseudoAction(name, aliases, help_)
            self._choices_actions.append(choice_action)

        # create the parser and add it to the map
        parser = self._parser_class(**kwargs)
        self._name_parser_map[name] = parser

        # make parser available under aliases also
        for alias in aliases:
            self._name_parser_map[alias] = parser

        return parser

    def _get_subactions(self):
        return self._choices_actions

    def __call__(self, parent, namespace, values, option_string=None):
        parser_name = values[0]
        arg_strings = values[1:]

        # set the parser name if requested
        if self.dest is not argparse.SUPPRESS:
            setattr(namespace, self.dest, parser_name)

        try:
            parser = self._name_parser_map[parser_name]
        except KeyError:
            args = {"parser_name": parser_name,
                    "choices": ", ".join(self._name_parser_map)}
            msg = _("unknown parser %(parser_name)r (choices: %(choices)s)") % args
            raise argparse.ArgumentError(self, msg)

        subnamespace, arg_strings = parser.parse_known_args(arg_strings)
        parent._parsed = (parser, subnamespace)

        if arg_strings:
            vars(namespace).setdefault(self._UNRECOGNIZED_ARGS_ATTR, [])
            getattr(namespace, self._UNRECOGNIZED_ARGS_ATTR).extend(arg_strings)
