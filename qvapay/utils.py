from inspect import signature
from typing import Any, Type, TypeVar

from httpx import Response

from .errors import QvaPayError

T = TypeVar("T")


def validate_response(response: Response) -> None:
    content_type = response.headers.get("content-type", "")
    is_html = "text/html" in content_type
    if not response.is_success or is_html:
        status = response.status_code if not is_html else 400
        message = None
        try:
            body = response.json()
            errors = body.get("errors")
            error = body.get("error")
            if isinstance(errors, list):
                message = "; ".join(str(e) for e in errors)
            elif isinstance(error, list):
                message = "; ".join(str(e) for e in error)
            else:
                message = error or body.get("message") or body.get("result")
        except Exception:
            pass
        raise QvaPayError(status, message)


def parse_json(cls: Type[T], **json: Any) -> T:
    cls_fields = {field for field in signature(cls).parameters}
    native_args, new_args = {}, {}
    for name, val in json.items():
        if name in cls_fields:
            native_args[name] = val
        else:
            new_args[name] = val
    ret = cls(**native_args)
    for new_name, new_val in new_args.items():
        setattr(ret, new_name, new_val)
    return ret
