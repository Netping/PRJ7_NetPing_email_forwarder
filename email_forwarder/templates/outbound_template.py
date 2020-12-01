import typing

from jinja2 import Environment


class OutboundTemplate:
    def __init__(self, **kwargs):
        self.template_id = kwargs.get('id', None)
        if not self.template_id:
            self.template_id = kwargs.get('template_id', None)
        self.inbound_template_id = kwargs.get('inbound_template_id', None)
        self.name = kwargs.get('name', None)
        self.template = kwargs.get('template', None)
        self.user = kwargs.get('user', None)

    def is_fit(self, user: str, inbound_template_id: int):
        if not self.user:
            return self.inbound_template_id == inbound_template_id
        else:
            return (self.user == user and
                    self.inbound_template_id == inbound_template_id)

    def html(self, values: dict):
        template = Environment().from_string(self.template)
        return template.render(values)
