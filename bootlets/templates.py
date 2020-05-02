from .base import Base, try_draw
from .decorators import inject


class Container(Base):
    block = '{content}'


class Div(Base):
    tag = 'div'

class P(Base):
    tag = 'p'

class H(Base):
    tag = 'h'
    defaults = {'size': 1}
    block = '<{tag}{size}{classes}>{content}</{tag}{size}>'

class Li(Base):
    tag = 'li'

class Ul(Base):
    tag = 'ul'

class UlList(Ul):
    defaults = {
        'ItemClass': Li,
        'item_kwargs': {}
    }

    def get_content(self):
        ItemClass = self.get('ItemClass')
        i_kwargs = self.get('item_kwargs')
        items = []
        for arg in self.args:
            item = ItemClass(arg, **i_kwargs) if ItemClass else arg
            items.append(try_draw(item))
        return '\n'.join(items)


class Dt(Base):
    tag = 'dt'
    defaults = {'class_':'col-sm-3'}


class Dd(Base):
    tag = 'dd'
    defaults = {'class_':'col-sm-9'}


class Dl(Base):
    tag = 'dl'

class DlDict(Dl):
    defaults = {
        'TitleClass': Dt,
        'title_kwargs': {},
        'DescClass': Dd,
        'desc_kwargs': {},
        'class_': 'row'
    }

    def get_content(self):
        TitleClass = self.get('TitleClass')
        t_kwargs = self.get('title_kwargs')
        DescClass = self.get('DescClass')
        d_kwargs = self.get('desc_kwargs')

        items = []
        for arg in self.args:
            if isinstance(arg, dict):
                for key, value in arg.items():
                    title = TitleClass(key, **t_kwargs) if TitleClass else key
                    desc = DescClass(value, **d_kwargs) if DescClass else value
                    items.append(try_draw(title) + try_draw(desc))
            else:
                raise NotImplementerError()
        return '\n'.join(items)

class Del(Base):
    tag = 'del'

class S(Base):
    tag = 's'

class Ins(Base):
    tag = 'ins'

class U(Base):
    tag = 'u'

class Small(Base):
    tag = 'small'

class Strong(Base):
    tag = 'strong'

class Em(Base):
    tag = 'em'

class Abbr(Base):
    tag = 'abbr'
    defaults = {
        'title': 'attribute'
    }
