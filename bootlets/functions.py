from .base import try_draw

def build_classes(self_):
    classes  = self_.kwargs.get('classes')
    if classes:
        if isinstance(classes, list):
            return ' class="' + ' '.join(classes) + '"'
        return ' class="' + classes + '"'
    return ''


def arg_content(self_):
    return '\n'.join([try_draw(arg) for arg in self_.args])


func_map = {
    'build_classes': build_classes,
    'arg_content': arg_content
}