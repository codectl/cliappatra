import inspect
from typing import Any, Callable, get_type_hints

from cliappatra.models import Field, FieldMeta


def get_func_params(func: Callable[..., Any]):
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)
    params = {}
    for param in signature.parameters.values():
        annotation = param.annotation
        if param.name in type_hints:
            annotation = type_hints[param.name]

        default = param.default
        field = default if isinstance(default, Field) else Field(default=default)
        field.meta = FieldMeta(
            name=param.name,
            kind=param.kind,
            annotation=annotation
        )
        params[param.name] = field
    return params
