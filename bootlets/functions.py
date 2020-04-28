from .base import try_draw

def arg_content(self_):
    return '\n'.join([try_draw(arg) for arg in self_.args])


func_map = {
    'arg_content': arg_content
}