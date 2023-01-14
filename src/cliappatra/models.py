import argparse
import inspect
from dataclasses import dataclass
from typing import Any, Optional, Union


@dataclass
class Field:
    default: Optional[Any] = None
    action: Optional[str] = None
    required: Optional[bool] = None
    nargs: Optional[Union[int, str]] = None
    envar: Optional[str] = None
    metavar: Optional[str] = None
    const: Optional[str] = None
    help: Optional[str] = None

    def asdict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}


class ParamMeta:

    def __init__(
            self,
            *,
            name: str,
            kind: int,
            default: Any = inspect.Parameter.empty,
            annotation: Any = inspect.Parameter.empty,
    ) -> None:
        self.name = name
        self.kind = kind
        self.default = default
        self.annotation = annotation
