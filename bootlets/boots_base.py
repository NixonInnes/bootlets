from logging import getLogger
from functools import lru_cache

from .funcs import list_to_str, try_draw
from .html import Div


class Boot:
    defaults = {}
    _class = ""

    def __init__(self, *args, **kwargs) -> None:
        self.logger = getLogger(self.__class__.__name__)
        self.args = args
        self.kwargs = kwargs
        self.init(*args, **{k: v for k, v in kwargs.items() if not k.startswith("_")})

    def __call__(self, *args, **kwargs):
        args = args if args else self.args
        kwargs = {**self.kwargs, **kwargs}
        return self.__class__(*args, **kwargs)

    def __iter__(self):
        return (arg for arg in self.args)

    def init(self, *args, **kwargs):
        pass

    def get(self, key, *args, **kwargs):
        return {**self.defaults, **self.kwargs}.get(key, *args, **kwargs)

    def get_class(self) -> str:
        s = ""
        if self._class:
            s += self._class
        optionals = self.build_classes()
        if optionals:
            s += " " + optionals
        if "class_" in self.kwargs:
            extra = list_to_str(self.kwargs["class_"])
            if extra:
                s += " " + extra
        return s

    def get_kwargs(self) -> dict:
        kwargs = {}
        for key, value in {**self.defaults, **self.kwargs}.items():
            if key.startswith("_"):
                continue
            if key == "class_":
                value = self.get_class()
            else:
                key = key.replace("_", "-")
                value = list_to_str(value)

            if key == "for_":
                key = "for"
            kwargs[key] = value
        if "class_" not in kwargs:
            c = self.get_class()
            if c:
                kwargs["class_"] = c
        return kwargs

    def build_classes(self) -> str:
        return ""

    def build_scripts(self):
        return []

    def build(self):
        return Div(*self.args, **self.get_kwargs())

    @lru_cache(maxsize=None)
    def _build(self):
        return self.build()

    def draw(self) -> str:
        return try_draw(self._build())

    def load(self):
        from .boots import Container

        content = self._build()
        scripts = try_get_scripts(content)
        if isinstance(content, (list, tuple)):
            content = Container(*content)
        return content, Container(*scripts)


def try_get_scripts(obj):
    scripts = []

    try:
        obj_scripts = obj.build_scripts()
        if isinstance(obj_scripts, (list, tuple)):
            scripts += obj.build_scripts()
        else:
            scripts.append(obj_scripts)
    except AttributeError:
        pass

    if isinstance(obj, (list, tuple, Boot)):
        for child in obj:
            scripts += try_get_scripts(child)

    try:
        scripts += try_get_scripts(obj._build())
    except AttributeError:
        pass

    return scripts
