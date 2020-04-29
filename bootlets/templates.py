from .base import Base, try_draw
from .decorators import inject


class Container(Base):
    funcs = ['arg_content']
    block = '{arg_content}'

    def arg_content(self):
        return '\n'.join([try_draw(arg) for arg in self.args])


class Div(Base):
    funcs = ['arg_content']
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
        'item_kwargs': {}
    }
    block = '<ul{classes}>{get_items}</ul>'

    def get_items(self):
        ItemClass = self.get('ItemClass')
        i_kwargs = self.get('item_kwargs')
        items = []
        for arg in self.args:
            item = ItemClass(arg, **i_kwargs) if ItemClass else arg
            items.append(try_draw(item))
        return '\n'.join(items)


class DescriptionListTitle(Base):
    arg_contracts = {'content': (str, list)}
    defaults = {'class_':'col-sm-3'}
    block = '<dt{classes}>{content}</dt>'


class DescriptionListDesc(Base):
    arg_contracts = {'content': (str, list)}
    defaults = {'class_':'col-sm-9'}
    block = '<dd{classes}>{content}</dd>'


class DescriptionList(Base):
    arg_contracts = {'content': dict}
    funcs = ['get_items']
    defaults = {
        'TitleClass': DescriptionListTitle,
        'title_kwargs': {},
        'DescClass': DescriptionListDesc,
        'desc_kwargs': {},
        'class_': 'row'
    }
    block = '<dl{classes}>{get_items}</dl>'

    def get_items(self):
        TitleClass = self.get('TitleClass')
        t_kwargs = self.get('title_kwargs')
        DescClass = self.get('DescClass')
        d_kwargs = self.get('desc_kwargs')

        items = []
        for key, value in self.get('content').items():
            title = TitleClass(key, **t_kwargs) if TitleClass else key
            desc = DescClass(value, **d_kwargs) if DescClass else value
            items.append(try_draw(title) + try_draw(desc))
        return '\n'.join(items)


