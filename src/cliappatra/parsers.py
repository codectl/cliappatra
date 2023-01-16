import abc
import inspect

from cliappatra.models import Field


class FieldParser:

    def __init__(self, parser):
        self._parser = parser

    def parse(self, field: Field):
        cls = _DefaultParser
        if field.meta.annotation is bool:
            cls = _BoolParser
        return cls(self._parser).parse(field)


class _BaseParser(abc.ABC):

    def __init__(self, parser):
        self._parser = parser

    @staticmethod
    @abc.abstractmethod
    def _parse_kwargs(kwargs: dict):
        pass

    def parse(self, field: Field):
        kwargs = field.asdict()
        meta = kwargs.pop("meta")

        if meta.kind == inspect.Parameter.POSITIONAL_ONLY:
            name = meta.name
            required = kwargs.pop("required")

            if "nargs" not in kwargs and not required:
                kwargs["nargs"] = "?"

            if "metavar" not in kwargs:
                kwargs["metavar"] = name.upper()

        else:
            name = f"--{meta.name}"

        # required = kwargs.pop("required")
        # env = kwargs.pop("envar")
        kwargs = self._parse_kwargs(kwargs)

        return self._parser.add_argument(name, **kwargs)


class _DefaultParser(_BaseParser):

    @staticmethod
    def _parse_kwargs(kwargs: dict):
        return kwargs


class _BoolParser(_BaseParser):

    @staticmethod
    def _parse_kwargs(kwargs: dict):
        return kwargs
