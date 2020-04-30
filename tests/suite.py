from hypothesis import given
import hypothesis.strategies as st

def decorator(*funcs):
    def wrapper(cls):
        for func in funcs:
            setattr(cls, func, func_suite[func])
        return cls
    return wrapper


def do_basic(test, *args, **kwargs):
    assert test.Template(*args, **kwargs)
    obj = test.Template(*args, **kwargs)
    assert obj.map_()
    assert obj.draw()


@given(s=st.text())
def test_single_str(self, s):
    do_basic(self)


@given(lst=st.lists(st.text()))
def test_list_strs(self, lst):
    do_basic(self)

func_suite = {
    'test_single_str': test_single_str,
    'test_list_strs': test_list_strs
}