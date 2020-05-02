from .base import Base
from . import templates


def get_html_tag_map():
    map_ = {}
    for t_name in dir(templates):
        try:
            template = getattr(templates, t_name)
            if issubclass(template, Base) and template.tag:
                map_[template.tag] = template
        except TypeError:
            continue
    return map_

HTML_MAP = get_html_tag_map()