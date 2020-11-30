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
            'select * from mails where outbound_templates is null;')
        self.templates = [OutboundTemplate(
            db=self.db, logs=self.logs, errors=self.errors,
            **template) for template in res]

    def all_templates(self, ) -> typing.List[OutboundTemplate]:
        if hasattr(self, 'templates'):
            return self.templates
        res = self.db.execute(
            'select * from mails where outbound_templates is null;')
        templates = [OutboundTemplate(
            db=self.db, logs=self.logs, errors=self.errors,
            **template) for template in res]
        return templates

    def template_by_inbound_template(self, inbound_template_id):
        if hasattr(self, 'templates'):
            return [template for template in self.templates
                    if template.inbound_template_id == inbound_template_id]
        res = self.db.execute(
            ('select * from mails where outbound_templates is null '
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
            ('select * from mails where outbound_templates is null '
             'where user= %s and inbound_template_id = %s;'),
            (user, inbound_template_id))
        templates = [OutboundTemplate(
            db=self.db, logs=self.logs, errors=self.errors,
            **template) for template in res]
        return templates
