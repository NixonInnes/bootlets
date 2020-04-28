from .base import Base, try_draw
from .decorators import inject


@inject('arg_content')
class Container(Base):
    funcs = []
    block = "{arg_content}"


@inject('arg_content', 'build_classes')
class Div(Base):
    funcs = []
    block = "<div{build_classes}>{arg_content}</div>"


@inject('build_classes')
class Paragraph(Base):
    funcs = []
    arg_names = ['text']
    block = "<p{build_classes}>{text}</p>"

P = Paragraph


@inject('build_classes')
class Header(Base):
    funcs = []
    arg_names = ['text']
    defaults = {'size': 1}
    block = "<h{size}{build_classes}>{text}</h{size}>"

H = Header


@inject('build_classes')
class ListItem(Base):
    arg_names = ['content']
    funcs = []
    block = "<li{build_classes}>{content}</li>"

Li = ListItem


@inject('build_classes')
class UnorderedList(Base):
    funcs = ['get_items']
    defaults = {'ItemClass': ListItem}
    block = "<ul{build_classes}>{get_items}</ul>"

    def get_items(self):
        ItemClass = self.get('ItemClass')
        if ItemClass:
            return '\n'.join([ItemClass(arg).draw() for arg in self.args])
        return '\n'.join(self.args)

