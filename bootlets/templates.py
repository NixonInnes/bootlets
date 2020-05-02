from .base import Base, try_draw


###################################################################################################
# Special Tags

class Container(Base):
    _block = '{content}'


class Comment(Base):
    _block = '<!-- {content} -->'


###################################################################################################
# A


class A(Base):
    tag = 'a'
    defaults = {
        'href': '#'
    }


class Abbr(Base):
    tag = 'abbr'
    defaults = {
        'title': 'attribute'
    }


class Address(Base):
    tag = 'address'


class Area(Base):
    tag = 'area'
    defaults = {
        'shape': 'rect',
        'coords': '0,0,0,0',
        'href': '#',
        'alt': 'Area'
    }


class Article(Base):
    tag = 'article'


class Aside(Base):
    tag = 'aside'


class Audio(Base):
    tag = 'audio'


###################################################################################################
# B

class B(Base):
    tag = 'b'


class Bdi(Base):
    tag = 'bdi'


class Bdo(Base):
    tag = 'bdo'
    defaults = {
        'dir': 'rtl'
    }


class Blockquote(Base):
    tag = 'blockquote'


class Body(Base):
    tag = 'body'


class Br(Base):
    closing = False
    tag = 'br'


class Button(Base):
    tag = 'button'
    defaults = {
        'type': 'button'
    }


###################################################################################################
# C

class Canvas(Base):
    tag = 'canvas'
    defaults = {
        'id': 'myCanvas'
    }


class Caption(Base):
    tag = 'caption'


class Cite(Base):
    tag = 'cite'


class Code(Base):
    tag = 'code'


class Col(Base):
    tag = 'col'


class ColGroup(Base):
    tag = 'colgroup'

###################################################################################################
# D

class Data(Base):
    tag = 'data'
    defaults = {
        'value': 0
    }


class DataList(Base):
    tag = 'datalist'
    defaults = {
        'id': 'MyDataList'
    }

class Dd(Base):
    tag = 'dd'


class Del(Base):
    tag = 'del'


class Details(Base):
    tag = 'details'


class Dfn(Base):
    tag = 'dfn'


class Dialog(Base):
    tag = 'dialog'
    defaults = {
        '_open': True
    }
    funcs = ['get_open']
    _block = '<{tag}{kwargs}{get_open}>{content}</{tag}>'

    def get_open(self):
        if self.defaults['_open']:
            return ' open'
        return ''


class Div(Base):
    tag = 'div'


class Dl(Base):
    tag = 'dl'


class Dt(Base):
    tag = 'dt'


class DlDict(Dl):
    TitleClass = Dt
    DescClass = Dd
    defaults = {
        '_title_kwargs': {},
        '_desc_kwargs': {},
    }

    def get_content(self):

        items = []
        for arg in self.args:
            if isinstance(arg, dict):
                for key, value in arg.items():
                    title = self.TitleClass(key, **self.get('_title_kwargs'))
                    desc = self.DescClass(value, **self.get('_desc_kwargs'))
                    items.append(try_draw(title) + try_draw(desc))
            else:
                raise NotImplementerError()
        return '\n'.join(items)


###################################################################################################
# E

class Em(Base):
    tag = 'em'


###################################################################################################
# F

class Footer(Base):
    tag = 'footer'


###################################################################################################
# G


###################################################################################################
# H

class H(Base):
    tag = 'h'
    defaults = {'size': 1}
    block = '<{tag}{size}{kwargs}>{content}</{tag}{size}>'


###################################################################################################
# I

class Ins(Base):
    tag = 'ins'


###################################################################################################
# J


###################################################################################################
# K


###################################################################################################
# L

class Li(Base):
    tag = 'li'


###################################################################################################
# M


###################################################################################################
# N


###################################################################################################
# O


###################################################################################################
# P

class P(Base):
    tag = 'p'


###################################################################################################
# Q


###################################################################################################
# R


###################################################################################################
# S

class S(Base):
    tag = 's'


class Small(Base):
    tag = 'small'


class Strong(Base):
    tag = 'strong'


###################################################################################################
# T


###################################################################################################
# U

class U(Base):
    tag = 'u'


class Ul(Base):
    tag = 'ul'


class UlList(Ul):
    ItemClass = Li
    defaults = {
        '_item_kwargs': {}
    }

    def get_content(self):
        items = []
        for arg in self.args:
            item = self.ItemClass(arg, **self.get('_item_kwargs'))
            items.append(try_draw(item))
        return '\n'.join(items)


###################################################################################################
# V


###################################################################################################
# W


###################################################################################################
# X


###################################################################################################
# Y


###################################################################################################
# Z

