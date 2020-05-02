import logging
from typing import Optional, Any, Type, TypeVar, List, Dict, Callable

BaseType = TypeVar('BaseType', bound='Base')

def try_draw(obj: Any) -> str:
    try:
        return obj.draw()
    except (AttributeError, TypeError):
        pass

    return str(obj)


class Base:
    closing : bool = True
    arg_contracts: Dict[str, Callable] = {}
    defaults: Dict[str, Any] = {}
    skip_kwargs: List[str] = []
    funcs: List[str] = []
    tag: str = ''
    _block = ''

    @property
    def block(self) -> str:
        if self._block:
            return self._block
        return '<{tag}{kwargs}>{content}</{tag}>' if self.closing else \
                 '<{tag}{kwargs} {content}>'

    def __init__(self, *args: Optional[Type[BaseType]],
                 **kwargs: Optional[Type[BaseType]]) -> None:
        self.__doc__ = self.__get_doc()
        self.logger = logging.getLogger(self.__class__.__name__)

        self.args = args
        self._kwargs = kwargs
        self.kwargs = {**{k:v for k,v in self.defaults.items() if not k.startswith('_')},
                       **kwargs}


    def __repr__(self) -> str:
        s = self.__class__.__qualname__ + '('
        if self.args:
            s += ', '.join([arg.__repr__() for arg in self.args])
        if self.kwargs:
            if self.args:
                s += ', '
            s += ', '.join([f'{k}={v.__repr__()}' for k,v in self._kwargs.items()])
        s += ')'
        return s

    # TODO: May need to write a wrapper to build and attach __doc__ to specific classes
    # so that it describes the default parameters
    def __get_doc(self) -> str:
        defaults_str = ', '.join(f'{k}={v}' for k,v in self.defaults.items())
        return f'{self.__class__.__name__}(*args, {defaults_str}, **kwargs)'


    def __call__(self, *args, **kwargs):
        args = args if args else self.args
        kwargs = {**self._kwargs, **kwargs}
        return self.__class__(*args, **kwargs)


    def get(self, key, *args, **kwargs) -> Any:
        return {**self.defaults, **self._kwargs}.get(key, *args, **kwargs)


    def map_(self) -> dict: # Returns a dict which we use in formatting the block of html
        map_ = {}

        for key, obj in self.kwargs.items():
            map_[key] = try_draw(obj)

        for f in self.funcs:
            map_[f] = try_draw(getattr(self, f)())

        map_['tag'] = self.tag
        map_['content'] = self.get_content()
        map_['kwargs'] = self.get_kwargs()

        return map_


    def get_content(self) -> str:
        return '\n'.join([try_draw(arg) for arg in self.args])

    def get_kwargs(self) -> str:
        s = ''
        if self.kwargs:
            for key, value in self.kwargs.items():
                if key in self.skip_kwargs:
                    continue
                if key == 'class_':
                    key = 'class'
                if isinstance(value, (list, tuple)):
                    value = ' '.join([v for v in value])
                s += f' {key}="{value}"'
        return s


    def draw(self) -> str: # Format the block string using dict generated in map_()
        return self.block.format(**self.map_())


class Generic(Base):
    def __init__(self, tag, *args, **kwargs) -> None:
        self.tag = tag
        if 'closing' in kwargs:
            self.closing = kwargs['closing']
            del kwargs['closing']
        super().__init__(*args, **kwargs)