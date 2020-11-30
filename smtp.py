import asyncore

from email_forwarder.config import VERSION, get_parser, get_loggers
from email_forwarder.db import create_db
from email_forwarder.mails.mailbox import MailBox
from email_forwarder.smtp_server.smtp_server import ProxySMTPServer


def run_smtp_proxy(config):
    log, error_log = get_loggers(config.log_dir, config.error_log_dir,
                                 'smtp.py')
    log.info(f'NetPIng Email forwarder v.{VERSION}, SMTP-Proxy server.')

    user_db = create_db(config.user_db_host, config.user_db_port,
                        config.user_db_username, config.user_db_password,
                        config.user_db_name)

    mailbox = MailBox(user_db, log, error_log)

    ProxySMTPServer((config.smtp_host, config.smtp_port),
                    (config.smtp_login, config.smtp_pass),
                    mailbox, log, error_log)
    asyncore.loop()


if __name__ == '__main__':
    config = get_parser(
        f'NetPIng Email forwarder v.{VERSION}, SMTP-Proxy server.',
        ('user_db', 'smtp')).parse_args()
    run_smtp_proxy(config)
