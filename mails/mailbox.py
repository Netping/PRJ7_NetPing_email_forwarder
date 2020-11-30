import logging
import typing

from db.DB import DB

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

    def get_user_mails(self, sender) -> typing.List[Mail, ...]:
        res = self.db.execute(('select * from mails where sender = %s;'),
                              (sender, ))
        return [Mail(db=self.db, logs=self.logs, errors=self.errors,
                     **mail) for mail in res]

    def new_mail(self, sender, receive_date, recieve_meta, body) -> Mail:
        res = self.db.execute(
            ('insert into mails(sender, receive_date, recieve_meta, body)'
             'values(%s, %s, %s, %s) returning id;'),
            (sender, receive_date, recieve_meta, body))
        return self.get_mail(res[0]['id'])

    def mail_queue(self) -> typing.List[Mail, ...]:
        res = self.db.execute(
            'select * from mails where inbound_template_id is null;')
        return [Mail(db=self.db, logs=self.logs, errors=self.errors,
                     **mail) for mail in res]
