import logging
import typing
import json

from email_forwarder.db.db import DB

from .mail import Mail


class MailBox:
    def __init__(self, db: DB, logs: logging.Logger, errors: logging.Logger):
        self.db = db
        self.logs = logs
        self.errors = errors

    def get_mail(self, mail_id) -> Mail:
        res = self.db.execute(('select * from mails where id = %s;'),
                              (mail_id, ))
        return Mail(db=self.db, logs=self.logs, errors=self.errors,
                    **res[0])

    def get_user_mails(self, sender) -> typing.List[Mail]:
        res = self.db.execute(('select * from mails where sender = %s;'),
                              (sender, ))
        return [Mail(db=self.db, logs=self.logs, errors=self.errors,
                     **mail) for mail in res]

    def get_user_template_mails(self, sender: str,
                                inbound_template_id: int) -> typing.List[Mail]:
        res = self.db.execute(
            ('select * from mails where sender = %s '
             'and inbound_template_id = %s;'),
            (sender, inbound_template_id))
        return [Mail(db=self.db, logs=self.logs, errors=self.errors,
                     **mail) for mail in res]

    def new_mail(self, sender, receive_date, recieve_meta, body) -> Mail:
        res = self.db.execute(
            ('insert into mails(sender, receive_date, receive_meta, body)'
             'values(%s, %s, %s, %s) returning id;'),
            (sender, receive_date, json.dumps(recieve_meta), body))
        return self.get_mail(res[0]['id'])

    def mail_queue(self) -> typing.List[Mail]:
        res = self.db.execute(
            'select * from mails where inbound_template_id is null;')
        return [Mail(db=self.db, logs=self.logs, errors=self.errors,
                     **mail) for mail in res]
