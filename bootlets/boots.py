from .funcs import list_to_str
from . import templates as t

class Boot:
    defaults = {}
    _class = ''

    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    def get(self, key, *args, **kwargs):
        return {**self.defaults, **self.kwargs}.get(key, *args, **kwargs)

    def get_class(self) -> str:
        s = ''
        if self._class:
            s += self._class
        optionals = self.build_classes()
        if optionals:
            s += ' ' + optionals
        if 'class_' in self.kwargs:
            extra = list_to_str(self.kwargs['class_'])
            if extra:
                s += ' ' + extra
        return s

    def get_kwargs(self) -> dict:
        kwargs = {}
        for key, value in {**self.defaults, **self.kwargs}.items():
            if key.startswith('_'):
                continue
            if key == 'class_':
                value = self.get_class()
            else:
                key = key.replace('_', '-')
                value = list_to_str(value)
            kwargs[key] = value
        if 'class_' not in kwargs:
            c = self.get_class()
            if c:
                kwargs['class_'] = c
        return kwargs

    def build_classes(self) -> str:
        return ''

    def build(self):
        raise NotImplementedError()

    def draw(self) -> str:
        return self.build().draw()


class Alert(Boot):
    _class = 'alert'
    defaults = {
        '_context': 'primary',
        'role': 'alert'
    }

    def build_classes(self):
        return f'alert-{self.get("_context")}'

    def build(self):
        return t.Div(*self.args,
                     **self.get_kwargs())


class AlertHeading(Boot):
    _class = 'alert-heading'
    defaults = {
        '_size': 4,
    }

    def build(self):
        return t.H(*self.args,
                   **self.get_kwargs())


class AlertDismissButton(Boot):
    _class = 'close'
    defaults = {
        'type': 'button',
        'data-dismiss': 'alert',
        'aria-label': 'Close'
    }
    def build(self):
        return t.Button(t.Span('&times;', aria_hidden='true'),
                        **self.get_kwargs())


class Badge(Boot):
    _class = 'badge'
    defaults = {
        '_context': 'primary'
    }

    def build_class(self):
        return f'badge-{self.get("_context")}'

    def build(self):
        return t.Span(*self.args,
                      **self.get_kwargs())


class BadgePill(Badge):
    _class = 'badge badge-pill'


class LinkBadge(Boot):
    _class = 'badge'
    defaults = {
        'href': '#',
        '_context': 'primary'
    }

    def build_class(self):
        return f'badge-{self.get("_context")}'

    def build(self):
        return t.A(*self.args,
                   **self.get_kwargs())


class BreadcrumbItem(Boot):
    _class = 'breadcrumb-item'
    defaults = {
        '_active': False
    }

    def build_classes(self):
        if self.get('_active'):
            return 'active'
        return ''

    def build(self):
        return t.Li(*self.args,
                    **self.get_kwargs())

class Breadcrumb(Boot):
    _class = 'breadcrumb'
    Li = BreadcrumbItem
    Ol = t.Ol
    Nav = t.Nav(aria_label='breadcrumb')
    def build(self):
        items = []
        for arg in self.args[:-1]:
            items.append(self.Li(arg))
        items.append(self.Li(self.args[-1],
                             _active=True,
                             aria_current='page'))
        return self.Nav(self.Ol(*items, **self.get_kwargs()))


class Button(Boot):
    defaults = {
        '_context': 'primary',
        '_size': 'md',
        '_outline': False,
        'type': 'button',
        '_block': False,
        '_disabled': False
    }

    sizes = {
        'sm': 'btn-sm',
        'md': '',
        'lg': 'btn-lg'
    }

    def get_class(self):
        s = 'btn'
        size_class = self.sizes.get(self.get('_size'))
        if size_class:
            s += ' ' + size_class
        s += ' btn-'
        if self.get('_outline'):
            s += 'outline-'
        s += self.get('_context')
        if self.get('_block'):
            s += ' btn-block'
        if self.get('_disabled'):
            s += ' disabled'
        return s

    def build(self):
        return t.Button(*self.args,
                        **self.get_kwargs())


class ButtonGroup(Boot):
    defaults = {
        'role': 'group',
        'size': 'md',
        '_vertical': False,
        'aria-label': 'myButtonGroup'
    }

    sizes = {
        'sm': 'btn-group-sm',
        'md': '',
        'lg': 'btn-group-lg'
    }

    def get_class(sels):
        s = 'btn-group'
        if self.get('_vertical'):
            s += '-vertical'
        size_class = self.sizes.get(self.get('_size'))
        if size_class:
            s += ' ' + size_classs
        return s

    def build(self):
        return t.Div(*self.args,
                     **self.get_kwargs())


class Card(Boot):
    _class = 'card'
    def build(self):
        return t.Div(*self.args,
                     **self.get_kwargs())


class CardBody(Boot):
    _class = 'card-body'
    def build(self):
        return t.Div(*self.args,
                     **self.get_kwargs())


class CardHeader(Boot):
    _class = 'card-header'
    def build(self):
        return t.Div(*self.args, **self.get_kwargs())


class CardFooter(Boot):
    _class = 'card-footer'
    def build(self):
        return t.Div(*self.args, **self.get_kwargs())


class CardTitle(Boot):
    _class = 'card-title'
    defaults = {
        'size': 5
    }
    def build(self):
        return t.H(*self.args, **self.get_kwargs())


class CardText(Boot):
    _class = 'card-text'
    def build(self):
        return t.P(*self.args, **self.get_kwargs())


class CardImage(Boot):
    defaults = {
        'src': '#',
        'alt': 'myCardImage',
        '_location': 'top'
    }
    def build_class(self):
        return f'card-img-{self.get("location")}'

    def build(self):
        return t.Img(**self.get_kwargs())


class ListGroup(Boot):
    _class = 'list-group'
    ListItem = t.Li(class_='list-group-item')
    defaults = {
        '_flush': False
    }

    def get_class(self):
        s = ''
        if self.get('_flush'):
            s += ' list-group-flush'
        return s

    def build(self):
        return t.Ul(*[self.ListItem(arg) for arg in self.args],
                    **self.get_kwargs())
