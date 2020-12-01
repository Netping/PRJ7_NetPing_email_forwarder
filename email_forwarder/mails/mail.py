"""
Mail module

Base class with parse and send functions.
"""
import typing
import json
import traceback
from datetime import datetime

import jinja2

from .sender import Sender
# from .mailbox import MailBox
from email_forwarder.templates.inbound_template import InboundTemplate


class Mail:
    """
    Mail class for processing recivied mails: parse and send

    Args:
        - id -- email id
        - receive_date -- mail receive date
        - receive_meta -- mail meta information
        - sender -- sender's email
        - body -- mail body
        - inbound_template_id -- template with which mail parsed
        - data -- extracted from mail body data
        - send_date -- date when mail sended to recivier
        - send_meta -- meta information of send mail
        - logs -- Logger object for info/debug log messages
        - errors -- Logger object for errors log messages
        - db -- DB object for work with database
    """
    def __init__(self, **kwargs):
        self.mail_id = kwargs.get('id', None)
        self.receive_date = kwargs.get('receive_date', None)
        self.receive_meta = kwargs.get('receive_meta', None)
        self.sender = kwargs.get('sender', None)
        self.body = kwargs.get('body', None)
        self.inbound_template_id = kwargs.get('inbound_template_id', None)
        self.data = kwargs.get('data', None)
        self.send_date = kwargs.get('send_date', None)
        self.send_meta = kwargs.get('send_meta', None)

        self.logs = kwargs.get('logs', None)
        self.errors = kwargs.get('errors', None)

        self.db = kwargs.get('db', None)

    def _save_parse_info(self, inbound_template_id: int,
                         data: typing.Optional[dict] = None) -> 'Mail':
        if inbound_template_id < 0:
            sql = ('update mails set inbound_template_id = %s where id = %s;')
            args = (inbound_template_id, self.mail_id)
        elif inbound_template_id >= 0 and data:
            sql = ('update mails set body = null, data = %s, '
                   'inbound_template_id = %s where id = %s;')
            args = (json.dumps(data), inbound_template_id, self.mail_id)
        else:
            return

        self.db.execute(sql, args)
        res = self.db.execute('select * from mails where id = %s',
                              (self.mail_id, ))
        return Mail(db=self.db, logs=self.logs, errors=self.errors, **res[0])

    def parse(self, templates: typing.List[InboundTemplate]) -> 'Mail':
        """
        Parse mail's body.
        If success save data and inbound template id, body set to null.
        Else set inbound template id to -1(minus one).
        In any case return new Mail object.

        Args:
            - templates -- list of template whom trying for text
        """
        self.logs.info('Извлечение данных из письма id:%s', self.mail_id)
        self.logs.info('Текст письма: %s', self.body)
        if self.inbound_template_id:
            self.errors.error('Ошибка, письмо id:%s уже обработано',
                              self.mail_id)
            raise Exception(f'Mail id:{self.mail_id} already parsed')
        if not self.body:
            self.errors.error('Ошибка, у письма id:%s нет текста',
                              self.mail_id)
            raise Exception(
                f'Mail id:{self.mail_id} have no body. Nothing to parse')

        inbound_template_id = -1
        data = None

        for template in templates:
            data = template.parse(self.body)
            if data:
                self.logs.info(('Извлечение данных из письма id:%s,'
                               'подобран шаблон входящих писем id:%s'),
                               self.mail_id, template.template_id)
                inbound_template_id = template.template_id
                break

        if inbound_template_id == -1:
            self.logs.info('Не удалось подобрать шаблон для письма id:%s',
                          self.mail_id)

        try:
            self.logs.info(('Сохранение извлеченных данных из письма id:%s, '
                           'данные:%s'), self.mail_id, data)
            return self._save_parse_info(inbound_template_id,
                                         data if data else None)
        except Exception as e:
            self.errors.error('Ошибка сохранения извлеченных данных: %s',
                              str(e))
            self.errors.error('Письмо %s', str(self.mail_id))
            self.errors.error('Идентификатор шаблона для входящих писем %s',
                              str(inbound_template_id))
            self.errors.error('Извлеченные данные %s', str(data))
            self.errors.error(traceback.format_exc())
            raise

    def _prepare_mail(self, mails: typing.List['Mail'],
                      template: jinja2.Template) -> str:
        """
        Prepare html text(html) using data from current mail
        and previos client(sender) mails parsed with the same
        inbound template.

        Args:
            - mails -- previous mails
            - template -- mail template
        """
        data = self.data
        data['mails'] = [mail.data for mail in mails]
        return template.html(data)

    def _save_send_info(self, send_meta: dict, send_date: datetime) -> 'Mail':
        """
        Save send info: meta and date.

        Args:
            - send_meta -- send mail meta information
            - send_date -- send date
        """
        self.db.execute(
            'update mails set send_meta = %s, send_date = %s where id = %s;',
            (json.dumps(send_meta), send_date, self.mail_id))
        res = self.db.execute('select * from mails where id = %s',
                              (self.mail_id, ))
        return Mail(db=self.db, logs=self.logs, errors=self.errors, **res[0])

    def send(self, sender: Sender, template_fabric,
             mailbox: 'MailBox') -> 'Mail':
        """
        Send mail to recipient.

        Args:
            - sender -- object with external smtp service
            - template_fabric -- outbound tamplate fabric object
            - mailbox -- mails fabric, for getting previous mails of user
                         parsed with the same inbound template
        """
        self.logs.info('Пересылка письма id:%s', self.mail_id)
        if not self.inbound_template_id:
            self.errors.error('Ошибка, письмо id:%s еще не обработано',
                              self.mail_id)
            raise Exception(f'Mail id:{self.mail_id} not parsed yet')
        if self.inbound_template_id < 0:
            self.errors.error('Ошибка, письмо id:%s не удалось обработать',
                              self.mail_id)
            raise Exception(
                f'Mail id:{self.mail_id} not parsed, template not found')

        outbound_template = self.get_template(template_fabric)
        if not outbound_template:
            self.errors.error(('Ошибка, для письма id:%s не удалось '
                               'подобрать шаблон для пересылки'),
                              self.mail_id)
            return self
        body = self._prepare_mail(
            mailbox.get_user_template_mails(self.sender,
                                            self.inbound_template_id),
            outbound_template)
        recipient = self.receive_meta.get('To', '')
        subject = self.receive_meta.get('Subject', '')
        self.logs.info('Отправление письма id:%s', self.mail_id)
        self.logs.info('Получатель:%s', recipient)
        self.logs.info('Заголовок:%s', subject)
        self.logs.info('Текст:%s', body)
        send_meta = sender.send(self.sender, recipient, subject, body)

        self.logs.info('Сохранение метаданных письма id:%s : %s',
                      self.mail_id, send_meta)
        return self._save_send_info(send_meta, datetime.now())

    def can_send(self) -> bool:
        return self.inbound_template_id >= 0

    def get_template(self, fabric):
        return fabric.get_user_template(self.sender, self.inbound_template_id)
