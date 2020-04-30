from hypothesis import given
import hypothesis.strategies as st

from suite import decorator

from bootlets.templates import Div, Paragraph, Header


class BaseTest:
    Template = None


@decorator('test_single_str',
           'test_list_strs')
class TestDiv(BaseTest):
    Template = Div

@decorator('test_single_str')
class TestParagraph(BaseTest):
    Template = Paragraph


@decorator('test_single_str')
class TestHeader(BaseTest):
    Template = Header

