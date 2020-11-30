import typing

from jinja2 import Environment


class OutboundTemplate:
    def __init__(self, template_id: int, inbound_template_id: int,
                 name: str, template: str, user: typing.Optional[str]):
        self.template_id = template_id
        self.inbound_template_id = inbound_template_id
        self.name = name
        self.template = template
        self.user = user

    def is_fit(self, user: str, inbound_template_id: int):
        if not self.user:
            return self.inbound_template_id == inbound_template_id
        else:
            return (self.user == user and
                    self.inbound_template_id == inbound_template_id)

    def html(self, values: dict):
        template = Environment().from_string(self.template)
        return template.render(values)
