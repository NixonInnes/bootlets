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
    arg_contracts: Dict[str, Callable] = {}
    defaults: Dict[str, Any] = {}
    funcs: List[str] = []
    block: str = ''

    def __init__(self, *args: Optional[Type[BaseType]],
                 **kwargs: Optional[Type[BaseType]]) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

        self.args = args
        self.arg_map = {}
        if self.arg_contracts:
            if len(args) != len(self.arg_contracts):
                raise TypeError(f'{self.__class__.__name__}() takes {len(self.arg_contracts)} '+
                                f'positional arguments but {len(args)} were given')

            self.arg_map = dict(zip(self.arg_contracts.keys(), args))

            # TODO: Use the arg_contracts to do some type checking

        self.kwargs = kwargs

    def __repr__(self) -> str:
        s = self.__class__.__qualname__ + '('
        if self.args:
            s += ', '.join([arg.__repr__() for arg in self.args])
        if self.kwargs:
            if self.args:
                s += ', '
            s += ', '.join([f'{k}={v.__repr__()}' for k,v in self.kwargs.items()])
        s += ')'
        return s


    def get(self, key, *args, **kwargs) -> Any:
        return {**self.defaults, **self.arg_map, **self.kwargs}.get(key, *args, **kwargs)


    def map_(self) -> dict: # Returns a dict which we use in formatting the block of html
        map_ = {}

        # Order of precedence: defaults < arg_map < kwargs < funcs

        for key, obj in self.defaults.items():
            if key in self.arg_contracts:
                self.logger.warn(f'{self.__class__.__name__}() default and positional argument '+
                                 f'with same name \'{key}\'. Argument will take precedence')
            map_[key] = try_draw(obj)

        for arg, obj in self.arg_map.items():
            map_[arg] = try_draw(obj)

        for key, obj in self.kwargs.items():
            if key in self.arg_contracts:
                self.logger.warn(f'{self.__class__.__name__}() keyword argument \'{key}\' '+
                                 f'overwriting positional argument with same name')
            map_[key] = try_draw(obj)

        for f in self.funcs:
            map_[f] = try_draw(getattr(self, f)())

        map_['classes'] = self.build_classes()

        return map_


    def build_classes(self):
        classes  = self.kwargs.get('class_')
        if classes:
            if isinstance(classes, list):
                return ' class="' + ' '.join(classes) + '"'
            return ' class="' + classes + '"'
        return ''


    def draw(self) -> str: # Format the block string using dict generated in map_()
        return self.block.format(**self.map_())