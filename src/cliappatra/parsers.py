import abc
import argparse
import inspect

from cliappatra.models import Field


class FieldParser:

    @staticmethod
    def parse(field: Field):
        cls = _DefaultParser
        if field.meta.annotation is bool:
            cls = _BoolParser
        return cls.parse(field)


class _BaseParser(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def _parse_kwargs(kwargs: dict):
        pass

    @classmethod
    def parse(cls, field: Field):
        kwargs = field.asdict()
        dest = field.meta.name
        meta = kwargs.pop("meta")

        if meta.kind == inspect.Parameter.POSITIONAL_ONLY:
            required = kwargs.pop("required", True)

            # enable optional arguments
            if "nargs" not in kwargs and not required:
                kwargs["nargs"] = argparse.OPTIONAL

            if "metavar" not in kwargs:
                kwargs["metavar"] = meta.name.upper()

        else:
            dest = f"--{dest}"

        args = (dest,)
        kwargs = cls._parse_kwargs(kwargs)
        return args, kwargs


class _DefaultParser(_BaseParser):

    @staticmethod
    def _parse_kwargs(kwargs: dict):
        return kwargs


class _BoolParser(_BaseParser):

    @staticmethod
    def _parse_kwargs(kwargs: dict):
        if "action" in kwargs:
            pass
        elif kwargs.get("required"):
            kwargs["action"] = argparse.BooleanOptionalAction
        elif kwargs.get("default"):
            kwargs["action"] = "store_true"
        else:
            kwargs["action"] = "store_false"
        return kwargs
