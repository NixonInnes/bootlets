from . import html
from .boots_base import Boot
from .funcs import try_draw


def raise_runtime_error(msg):
    def inner(*args, **kwargs):
        raise RuntimeError(msg)
    return inner

try:
    from wtforms.fields import HiddenField
except ImportError:
    is_hidden_field_filter = raise_runtime_error("WTForms is not installed.")
else:
    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

try:
    from flask import url_for, request
except ImportError:
    url_for = raise_runtime_error("Flask is not installed.")
    request = raise_runtime_error("Flask is not installed.")




class Container(Boot):
    defaults = {"_inline": False}
    _block = "{content}"

    def build(self):
        if self.get("_inline"):
            joinstr = " "
        else:
            joinstr = "\n"
        return joinstr.join([try_draw(item) for item in self])


class Alert(Boot):
    _class = "alert"
    defaults = {"_context": "primary", "role": "alert"}

    def build_classes(self):
        return f'alert-{self.get("_context")}'

    def build(self):
        return html.Div(*self.args, **self.get_kwargs())


class AlertHeading(Boot):
    _class = "alert-heading"
    defaults = {
        "_size": 4,
    }

    def build(self):
        return html.H(*self.args, **self.get_kwargs())


class AlertDismissButton(Boot):
    _class = "close"
    defaults = {"type": "button", "data-dismiss": "alert", "aria-label": "Close"}

    def build(self):
        return html.Button(
            html.Span("&times;", aria_hidden="true"), **self.get_kwargs()
        )


class Badge(Boot):
    _class = "badge"
    defaults = {"_context": "primary"}

    def get_class(self):
        return f'{self._class} badge-{self.get("_context")}'

    def build(self):
        return html.Span(*self.args, **self.get_kwargs())


class BadgePill(Badge):
    _class = "badge badge-pill"


class LinkBadge(Boot):
    _class = "badge"
    defaults = {
        "_context": "primary",
        "href": "#",
    }

    def build_class(self):
        return f'badge-{self.get("_context")}'

    def build(self):
        return html.A(*self.args, **self.get_kwargs())


class BreadcrumbItem(Boot):
    _class = "breadcrumb-item"
    defaults = {"_active": False}

    def build_classes(self):
        if self.get("_active"):
            return "active"
        return ""

    def build(self):
        return html.Li(*self.args, **self.get_kwargs())


class Breadcrumb(Boot):
    _class = "breadcrumb"
    Li = BreadcrumbItem
    Ol = html.Ol
    Nav = html.Nav(aria_label="breadcrumb")

    def build(self):
        items = []
        for arg in self.args[:-1]:
            items.append(self.Li(arg))
        items.append(self.Li(self.args[-1], _active=True, aria_current="page"))
        return self.Nav(self.Ol(*items, **self.get_kwargs()))


class Button(Boot):
    defaults = {
        "_context": "primary",
        "_size": "md",
        "_outline": False,
        "_block": False,
        "_disabled": False,
        "type": "button",
    }

    sizes = {"sm": "btn-sm", "md": "", "lg": "btn-lg"}

    def get_class(self):
        s = "btn"
        size_class = self.sizes.get(self.get("_size"))
        if size_class:
            s += " " + size_class
        s += " btn-"
        if self.get("_outline"):
            s += "outline-"
        s += self.get("_context")
        if self.get("_block"):
            s += " btn-block"
        if self.get("_disabled"):
            s += " disabled"
        return s

    def build(self):
        return html.Button(*self.args, **self.get_kwargs())


class ButtonLink(Boot):
    defaults = {
        "_context": "primary",
        "_size": "md",
        "_outline": False,
        "_block": False,
        "_disabled": False,
        "type": "button",
    }

    sizes = {"sm": "btn-sm", "md": "", "lg": "btn-lg"}

    def get_class(self):
        s = "btn"
        size_class = self.sizes.get(self.get("_size"))
        if size_class:
            s += " " + size_class
        s += " btn-"
        if self.get("_outline"):
            s += "outline-"
        s += self.get("_context")
        if self.get("_block"):
            s += " btn-block"
        if self.get("_disabled"):
            s += " disabled"
        return s

    def build(self):
        return html.A(*self.args, **self.get_kwargs())


class ButtonGroup(Boot):
    defaults = {
        "_vertical": False,
        "role": "group",
        "size": "md",
        "aria-label": "myButtonGroup",
    }

    sizes = {"sm": "btn-group-sm", "md": "", "lg": "btn-group-lg"}

    def get_class(self):
        s = "btn-group"
        if self.get("_vertical"):
            s += "-vertical"
        size_class = self.sizes.get(self.get("_size"))
        if size_class:
            s += " " + size_class
        return s


class Card(Boot):
    _class = "card mb-3"


class CardBody(Boot):
    _class = "card-body"


class CardHeader(Boot):
    _class = "card-header"
    defaults = {"_size": 4}

    def build(self):
        return html.H(*self.args, _size=self.get("_size"), **self.get_kwargs())


class CardFooter(Boot):
    _class = "card-footer"


class CardTitle(Boot):
    _class = "card-title"
    defaults = {"_size": 5}

    def build(self):
        return html.H(*self.args, _size=self.get("_size"), **self.get_kwargs())


class CardText(Boot):
    _class = "card-text"

    def build(self):
        return html.P(*self.args, **self.get_kwargs())


class CardImage(Boot):
    defaults = {
        "_location": "top",
        "src": "#",
        "alt": "myCardImage",
    }

    def build_class(self):
        return f'card-img-{self.get("location")}'

    def build(self):
        return html.Img(**self.get_kwargs())


class DescriptionList(Boot):
    defaults = {"_column_widths": (3, 9)}

    def build(self):
        if len(self.args) == 1:
            arg = self.args[0]
            if isinstance(arg, dict):
                iterable = arg.items()
            else:
                iterable = arg
        else:
            iterable = self.args

        lhs_col_size = self.get("_column_widths")[0]
        rhs_col_size = self.get("_column_widths")[1]

        return Container(
            html.Dl(class_="row")(
                *[
                    Container(
                        html.Dt(class_=f"col-sm-{lhs_col_size}")(dt),
                        html.Dd(class_=f"col-sm-{rhs_col_size}")(dd),
                    )
                    for dt, dd in iterable
                ]
            )
        )


class ListGroup(Boot):
    _class = "list-group"
    Li = html.Li
    defaults = {"_flush": False, "_li_class": "list-group-item"}

    def build_classes(self):
        s = ""
        if self.get("_flush"):
            s += " list-group-flush"
        return s

    def build(self):
        return html.Ul(
            *[self.Li(arg, class_=self.get("_li_class")) for arg in self.args],
            **self.get_kwargs(),
        )


class Accordian(Boot):
    _class = "accordian"
    defaults = {"id": "myAccordian"}


class Dropdown(Boot):
    _class = "dropdown"


class DropdownItem(Boot):
    _class = "dropdown-item"
    defaults = {
        "href": "#",
    }

    def build(self):
        return html.A(*self.args, **self.get_kwargs())


class DropdownMenu(Boot):
    _class = "dropdown-menu"
    defaults = {
        "aria-labelledby": "myDropdownMenu",
    }


class DropdownDivider(Boot):
    _class = "dropdown-divider"


class DropdownButton(Boot):
    _class = "btn"
    defaults = {
        "_context": "primary",
        "data-toggle": "dropdown",
        "aria-haspopup": "true",
        "aria-expanded": "false",
    }

    def build_class(self):
        return "btn-" + self.get("_context") + "dropdown-toggle"

    def build(self):
        return html.Button(*self.args, **self.get_kwargs())


class Table(Boot):
    _class = "table table-hover"

    defaults = {
        "_headers": [],
        "_rows": [],
        "_hover": True,
    }

    def build(self):
        headers = html.THead(
            html.Tr(*[html.Th(i, scope="col") for i in self.get("_headers")])
        )
        rows = html.TBody(
            *[html.Tr(*[html.Td(i) for i in row]) for row in self.get("_rows")]
        )

        return html.Table(headers, rows, **self.get_kwargs())


class FormField(Boot):
    defaults = {
        "_form_type": "basic",
        "_button_map": {},
    }

    def build(self):
        field = self.args[0]

        if field.type == "SubmitField":
            btn_cls = self.get("_button_map").get(field.name, "primary")
            return field(class_=f"btn btn-{btn_cls}")
            # return html.Button(class_=f'btn btn-{btn_cls}')

        elif field.type == "RadioField":
            return Container(
                *[html.Div(class_="form-check")(item(), item.label()) for item in field]
            )

        elif field.type == "FormField":
            return html.FieldSet()(
                html.Legend()(field.label),
                *[
                    FormField(
                        item,
                        _form_type=self.get("_form_type"),
                        _button_map=self.get("_button_map"),
                    )
                    for item in field
                    if not is_hidden_field_filter(item)
                ],
            )

        elif field.type == "BooleanField":
            return html.Div(class_="form-group form-check")(
                field(class_="form-check-input"), field.label(class_="form-check-label")
            )

        elif field.type == "FileField" or field.type == "MultiplFileField":
            return html.Div(class_="form-group")(
                field.label(), field(class_="form-control-file")
            )

        else:
            if is_hidden_field_filter(field):
                return html.Div(class_="form-group")(field())
            return html.Div(class_="form-group")(
                field.label(), field(class_="form-control")
            )


class QuickForm(Boot):
    defaults = {
        "_action": "",
        "_method": "post",
        "_extra_classes": None,
        "_role": "form",
        "_form_type": "basic",
        "_columns": ("lg", 2, 10),
        "_enctype": None,
        "_button_map": {},
        "_id": "",
        "_novalidate": False,
        "_render_kw": {},
    }

    def build(self):
        form = self.args[0]
        return html.Form(
            Container(
                *[
                    FormField(
                        field,
                        _form_type=self.get("_form_type"),
                        _columns=self.get("_columns"),
                        _button_map=self.get("_button_map"),
                    )
                    for field in form
                ]
            )
        )


class Modal(Boot):
    defaults = {"_id": "modal_id", "_title": "Modal", "_tabindex": -1}

    def build(self):
        return html.Div(
            class_="modal fade",
            id=f'Modal_{self.get("_id")}',
            tabindex=self.get("_tabindex"),
            role="dialog",
            aria_labelledby=f'ModalLabel_{self.get("_id")}',
            aria_hidden="true",
        )(
            html.Div(class_="modal-dialog modal-dialog-centered", role="document")(
                html.Div(class_="modal-content")(
                    html.Div(class_="modal-header")(
                        html.H(
                            size=5,
                            class_="modal-title",
                            id=f'ModalLabel-{self.get("_id")}',
                        )(self.get("_title")),
                        html.Button(
                            type="button",
                            class_="close",
                            data_bs_dismiss="modal",
                            aria_label="Close",
                        )(html.Span(aria_hidden="true")("&times;")),
                    ),
                    html.Div(class_="modal-body")(*self.args),
                    self.get_footer(),
                )
            )
        )

    def get_footer(self):
        if self.get("_footer"):
            return html.Div(class_="modal-footer")(self.get("_footer"))
        return ""


class ModalButton(Boot):
    defaults = {
        "_id": "modal_id",
        "_text": "Submit",
        "_context": "primary",
    }

    def build(self):
        return html.Button(
            type="button",
            class_=f'btn btn-{self.get("_context")}{self.get_class()}',
            data_bs_toggle="modal",
            data_bs_target=f'#Modal_{self.get("_id")}',
        )(self.get("_text"))


class ModalLink(Boot):
    defaults = {
        "_id": "modal_id",
        "_context": "primary",
    }

    def build(self):
        return html.A(
            type="button",
            data_toggle="modal",
            data_target=f'#Modal_{self.get("_id")}',
            **self.get_kwargs(),
        )(*self.args)


class Pagination(Boot):
    def init(self, *args, **kwargs):
        self.pagination = args[0]
        self.endpoint = args[1]

    defaults = {
        "_label": "Pagination",
        "_request_param": "page",
        "_url_kwargs": {},
        "_fragment": "",
    }

    def get_prev_endpoint(self):
        if self.pagination.has_prev:
            return (
                url_for(
                    self.endpoint,
                    **{
                        **request.args,
                        **{self.get("_request_param"): self.pagination.prev_num},
                        **self.get("_url_kwargs"),
                    },
                )
                + self.get("_fragment")
            )
        return "#"

    def get_next_endpoint(self):
        if self.pagination.has_next:
            return (
                url_for(
                    self.endpoint,
                    **{
                        **request.args,
                        **{self.get("_request_param"): self.pagination.next_num},
                        **self.get("_url_kwargs"),
                    },
                )
                + self.get("_fragment")
            )
        return "#"

    def get_pages(self):
        page_list_items = []
        for page in self.pagination.iter_pages():
            if page is not None:
                if page == self.pagination.page:
                    page_list_items.append(
                        html.Li(class_="page-item active")(
                            html.Span(page, class_="page-link")
                        )
                    )
                else:
                    page_list_items.append(
                        html.Li(class_="page-item")(
                            html.A(
                                page,
                                class_="page-link",
                                href=url_for(
                                    self.endpoint,
                                    **{
                                        **request.args,
                                        **{self.get("_request_param"): page},
                                        **self.get("_url_kwargs"),
                                    },
                                ),
                            )
                        )
                    )

        prev_page_list_item_class = "page-item"
        if not self.pagination.has_prev:
            prev_page_list_item_class += " disabled"

        prev_page_list_item = html.Li(class_=prev_page_list_item_class)(
            html.A("&laquo", class_="page-link", href=self.get_prev_endpoint())
        )

        next_page_list_item_class = "page-item"
        if not self.pagination.has_next:
            next_page_list_item_class += " disabled"
        next_page_list_item = html.Li(class_=next_page_list_item_class)(
            html.A("&raquo", class_="page-link", href=self.get_next_endpoint())
        )

        return [prev_page_list_item, *page_list_items, next_page_list_item]

    def build(self):
        return html.Nav(aria_label=self.get("_label"))(
            html.Ul(class_="pagination justify-content-center")(*self.get_pages())
        )
