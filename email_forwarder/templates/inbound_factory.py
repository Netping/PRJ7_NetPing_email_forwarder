import logging
import typing

from email_forwarder.db.db import DB
from .inbound_template import InboundTemplate


class InboundFactory:
    def __init__(self, db: DB, logs: logging.Logger, errors: logging.Logger):
        self.db = db
        self.logs = logs
        self.errors = errors

    def fill(self):
        res = self.db.execute(
            'select * from mails where inbound_template_id is null;')
        self.templates = [InboundTemplate(
            db=self.db, logs=self.logs, errors=self.errors,
            **template) for template in res]

    def all_templates(self) -> typing.List[InboundTemplate]:
        return self.templates
