from .base import Base, try_draw
from .decorators import inject


class Container(Base):
    block = '{arg_content}'

    def arg_content(self):
        return '\n'.join([try_draw(arg) for arg in self.args])


class Div(Base):
    block = '<div{classes}>{arg_content}</div>'

    def arg_content(self):
        return '\n'.join([try_draw(arg) for arg in self.args])


class Paragraph(Base):
    arg_contracts = {'text': str}
    block = '<p{classes}>{text}</p>'

P = Paragraph


class Header(Base):
    arg_contracts = {'text': str}
    defaults = {'size': 1}
    block = '<h{size}{classes}>{text}</h{size}>'

H = Header


class ListItem(Base):
    arg_contracts = {'content': (str, list)}
    block = '<li{classes}>{content}</li>'

Li = ListItem


class UnorderedList(Base):
    funcs = ['get_items']
    defaults = {
        'ItemClass': ListItem,
        'item_args': [],
        'item_kwargs': {}
    }
    block = '<ul{classes}>{get_items}</ul>'

    def get_items(self):
        ItemClass = self.get('ItemClass')
        if ItemClass:
            return '\n'.join([ItemClass(arg, *self.get('item_args'),
                                        **self.get('item_kwargs')).draw() for arg in self.args])
        return '\n'.join(self.args)


class DescriptionListTitle(Base):
    arg_contracts = {'content': (str, list)}
    defaults = {'class_':'col-sm-3'}
    block = '<dt{classes}>{content}</dt>'


class DescriptionListDesc(Base):
    arg_contracts = {'content': (str, list)}
    defaults = {'class_':'col-sm-9'}
    block = '<dd{classes}>{content}</dd>'


class DescriptionList(Base):
    arg_contracts = {'content': (str, list)}
    funcs = ['get_items']
    defaults = {
        'TitleClass': DescriptionListTitle,
        'title_kwargs': {},
        'DescClass': DescriptionListDesc,
        'desc_kwargs': {},
        'class_': 'row'
    }
    block = '<dl{class}>{get_items}</dl>'

    def get_items(self):
        assert isinstance(self.get('content'), dict), f'Expected dictionary for '


