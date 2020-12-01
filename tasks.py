import time
import traceback

from email_forwarder.config import VERSION, get_parser, get_loggers
from email_forwarder.db import create_db
from email_forwarder.mails.smtp2go import SMTP2GO
from email_forwarder.mails.mailbox import MailBox
from email_forwarder.templates.inbound_factory import InboundFactory
from email_forwarder.templates.outbound_factory import OutboundFactory
from email_forwarder.templates.factory_wrapper import FactoryWrapper


def run_tasks(config):
    log, error_log = get_loggers(config.log_dir, config.error_log_dir,
                                 'tasks.py')
    log.info(f'NetPIng Email forwarder v.{VERSION}, Tasks.')

    admin_db = create_db(config.admin_db_host, config.admin_db_port,
                         config.admin_db_username, config.admin_db_password,
                         config.admin_db_name)

    user_db = create_db(config.user_db_host, config.user_db_port,
                        config.user_db_username, config.user_db_password,
                        config.user_db_name)

    mailbox = MailBox(user_db, log, error_log)

    sender = SMTP2GO(config.smtp2go_host, config.smtp2go_port,
                     config.smtp2go_user, config.smtp2go_pass, log, error_log)

    inbound_templates = InboundFactory(admin_db, log, error_log)
    inbound_templates.fill()
    outbound_admin_templates = OutboundFactory(admin_db, log, error_log)
    outbound_admin_templates.fill()
    outbound_user_templates = OutboundFactory(user_db, log, error_log)
    outbound_factory = FactoryWrapper(outbound_admin_templates,
                                      outbound_user_templates, log)

    while True:
        emails = mailbox.mail_queue()
        for email in emails:
            try:
                log.info('Обработка письма %s', email.mail_id)
                log.info('Обработка письма, получено %s', email.receive_date)
                log.info('Обработка письма, отправитель %s', email.sender)
                log.info('Обработка письма, мета информация %s',
                         email.receive_meta)
                log.info('Обработка письма, содержание %s', email.body)
                email = email.parse(inbound_templates.all_templates())
                if email.can_send():
                    log.info('Отправление письма %s', email.mail_id)
                    email = email.send(sender, outbound_factory, mailbox)
            except Exception as e:
                error_log.error('Ошибка обработки письма %s: %s',
                                email.mail_id, str(e))
                error_log.error(traceback.format_exc())
        time.sleep(5)


if __name__ == '__main__':
    config = get_parser(f'NetPIng Email forwarder v.{VERSION}, Tasks.',
                        ('user_db', 'admin_db', 'smtp2go')).parse_args()
    run_tasks(config)
