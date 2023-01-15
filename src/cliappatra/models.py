import inspect
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Union


@dataclass
class FieldMeta:
    name: str
    kind: Enum
    annotation: Any = inspect.Parameter.empty


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
    meta: Optional[FieldMeta] = None

    def asdict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}
