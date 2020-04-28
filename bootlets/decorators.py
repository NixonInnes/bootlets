from .base import try_draw
from .functions import func_map


def add_func_to_template(template, func_name, alt_name=None):
    if func_name in template.funcs:
        return

    func = func_map.get(func_name)
    if not func:
        raise LookupError(f'Unable to find template function \'{func_name}\'')

    if not alt_name:
        template.funcs.append(func_name)
        setattr(template, func_name, func)
    else:
        template.funcs.append(alt_name)
        setattr(template, alt_name, func)


#def inject(*inj_args, **inj_kwargs):
def inject(*inj_args):
    def outer(cls_):
        for func_name in inj_args:
            add_func_to_template(cls_, func_name)

        #for alt_name, func_name in inj_kwargs:
        #    add_func_to_template(cls_, func_name, alt_name=alt_name)

        def inner(*args, **kwargs):
            obj = cls_(*args, **kwargs)
            return obj

        return inner

    return outer
