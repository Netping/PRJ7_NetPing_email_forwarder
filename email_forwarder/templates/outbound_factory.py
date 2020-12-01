import logging
import typing

from email_forwarder.db.db import DB
from .outbound_template import OutboundTemplate


class OutboundFactory:
    def __init__(self, db: DB, logs: logging.Logger, errors: logging.Logger):
        self.db = db
        self.logs = logs
        self.errors = errors

    def fill(self):
        res = self.db.execute(
            'select * from outbound_templates;')
        self.templates = [OutboundTemplate(**template) for template in res]

    def all_templates(self, ) -> typing.List[OutboundTemplate]:
        if hasattr(self, 'templates'):
            return self.templates
        res = self.db.execute(
            'select * from outbound_templates;')
        templates = [OutboundTemplate(
            db=self.db, logs=self.logs, errors=self.errors,
            **template) for template in res]
        return templates

    def template_by_inbound_template(self, inbound_template_id):
        if hasattr(self, 'templates'):
            return [template for template in self.templates
                    if template.inbound_template_id == inbound_template_id]
        res = self.db.execute(
            ('select * from outbound_templates '
             'where inbound_template_id = %s;'),
            (inbound_template_id, ))
        templates = [OutboundTemplate(
            db=self.db, logs=self.logs, errors=self.errors,
            **template) for template in res]
        return templates

    def template_by_user(self, user, inbound_template_id):
        if hasattr(self, 'templates'):
            return [template for template in self.templates
                    if template.user == user and
                    template.inbound_template_id == inbound_template_id]
        res = self.db.execute(
            ('select * from outbound_templates '
             'where user= %s and inbound_template_id = %s;'),
            (user, inbound_template_id))
        templates = [OutboundTemplate(
            db=self.db, logs=self.logs, errors=self.errors,
            **template) for template in res]
        return templates[0] if templates else None

    def save_template_for_user(self, user: str, inbound_template_id: int,
                               name: str, template: str):
        sql = '''
        insert into outbound_templates(user, inbound_template_id,
                                       name, template)
        values(%s,%s, %s, %s)
        on conflict on constraint one_outbound_template
        do
            update set template = %s
        returning id;
        '''
        res = self.db.execute(sql,
                              (user, inbound_template_id, name, template))
        return OutboundTemplate(
            db=self.db, logs=self.logs, errors=self.errors, **res[0])
