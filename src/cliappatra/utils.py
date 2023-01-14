import inspect
from typing import Any, Callable, get_type_hints

from cliappatra.models import ParamMeta


def get_func_params(func: Callable[..., Any]):
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)
    params = {}
    for param in signature.parameters.values():
        annotation = param.annotation
        if param.name in type_hints:
            annotation = type_hints[param.name]
        params[param.name] = ParamMeta(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=annotation
        )
    return params
