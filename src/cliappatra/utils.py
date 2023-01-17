import argparse
import inspect
from typing import Any, Callable, get_type_hints

from cliappatra.models import Field, FieldMeta


def get_func_fields(func: Callable[..., Any]):
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)
    fields = {}
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
        fields[param.name] = field
    return fields


def fields_to_params(
        namespace: argparse.Namespace,
        fields: dict[str, Field],
) -> (list[Any], dict[str, Any]):
    args = []
    kwargs = {}
    kv = vars(namespace)
    for k, v in kv.items():
        if fields[k].meta.kind == inspect.Parameter.POSITIONAL_ONLY:
            args.append(v)
        else:
            kwargs[k] = v
    return args, kwargs
