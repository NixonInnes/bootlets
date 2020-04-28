import logging


def try_draw(obj):
    try:
        return obj.draw()
    except AttributeError:
        return obj


class Base:
    arg_names = []
    defaults = {}

    funcs = []
    block = ''

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.args = args
        if self.arg_names:
            if len(args) != len(self.arg_names):
                raise TypeError(f'{self.__class__.__name__}() takes {len(self.arg_names)} '+
                                f'positional arguments but {len(args)} were given')

            self.arg_map = dict(zip(self.arg_names, args))
        else:
            self.arg_map = {}

        self.kwargs = kwargs


    def get(self, key):
        return {**self.defaults, **self.arg_map, **self.kwargs}.get(key)


    def map_(self): # Returns a dict which we use in formatting the block of html
        map_ = {}

        for arg, obj in self.arg_map.items():
            map_[arg] = try_draw(obj)

        for key, obj in self.defaults.items():
            if key in map_:
                self.logger.warn(f'{self.__class__.__name__}() default \'{key}\' '+
                                     f' overwriting positional argument with same name')
            map_[key] = try_draw(obj)

        for key, obj in self.kwargs.items():
            if key in map_:
                self.logger.warn(f'{self.__class__.__name__}() keyword argument \'{key}\' '+
                                 f' overwriting positional argument with same name')
            map_[key] = try_draw(obj)

        for f in self.funcs:
            map_[f] = getattr(self, f)()

        return map_


    def draw(self): # Format the block string using dict generated in map_()
        return self.block.format(**self.map_())