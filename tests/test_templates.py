import logging
import unittest
from hypothesis import given
import hypothesis.strategies as st

from bootlets.base import Base
from bootlets.templates import Container, H


@unittest.skip()
class BaseTest(unittest.TestCase):
    Template = None

    def setUp(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def do_basic(self, *args, **kwargs):
        self.logger.info('Can create...')
        assert self.Template(*args, **kwargs)
        obj = self.Template(*args, **kwargs)
        self.logger.info('Can map_()')
        assert obj.map_()
        self.logger.info('Can draw()')
        assert obj.draw()

    @given(s=st.text())
    def test_repl(self, s):
        obj = self.Template(s)
        exec('exec_draw = '+obj.__repr__()+'.draw()')

    @given(s=st.text())
    def test_single_str(self, s):
        self.do_basic(self, s)

    @given(lst=st.lists(st.text()))
    def test_list_strs(self, lst):
        self.do_basic(self, lst)


class TestBase(BaseTest):
    Template = Base


class TestContainer(BaseTest):
    Template = Container


class TestH(BaseTest):
    Template = H

    @given(s=st.text(), title=st.text())
    def test_single_str(self, s, title):
        self.do_basic(s, title=title)