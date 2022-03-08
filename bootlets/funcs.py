from typing import Any


def try_draw(obj: Any) -> str:
    try:
        obj = obj._build()
    except AttributeError:
        pass

    try:
        return obj.draw()
    except (AttributeError, TypeError):
        pass

    return str(obj)


def list_to_str(obj) -> str:
    if isinstance(obj, str):
        return obj
    if isinstance(obj, (list, tuple)):
        return " ".join(obj)
    return str(obj)
