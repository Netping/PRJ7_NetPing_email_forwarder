from email_forwarder.config import VERSION, get_parser, get_loggers
from email_forwarder.db import create_db
from email_forwarder.mails.mailbox import MailBox
from email_forwarder.templates.inbound_factory import InboundFactory
from email_forwarder.templates.outbound_factory import OutboundFactory
from email_forwarder.web.server import WebServer


def run_web(config):
    log, error_log = get_loggers(config.log_dir, config.error_log_dir,
                                 'web.py')
    log.info(f'NetPIng Email forwarder v.{VERSION}, WEB.')

    admin_db = create_db(config.admin_db_host, config.admin_db_port,
                         config.admin_db_username, config.admin_db_password,
                         config.admin_db_name)

    user_db = create_db(config.user_db_host, config.user_db_port,
                        config.user_db_username, config.user_db_password,
                        config.user_db_name)

    inbound_factory = InboundFactory(admin_db, log, error_log)
    inbound_factory.fill()
    outbound_factory = OutboundFactory(admin_db, log, error_log)
    outbound_factory.fill()
    factory = OutboundFactory(user_db, log, error_log)
    mailbox = MailBox(user_db, log, error_log)
    server = WebServer(config.web_host, config.web_port,
                       inbound_factory.all_templates(),
                       outbound_factory.all_templates(),
                       factory, mailbox, log, error_log)
    server.run()


if __name__ == '__main__':
    config = get_parser(f'NetPIng Email forwarder v.{VERSION}, WEB.',
                        ('user_db', 'admin_db', 'web')).parse_args()
    run_web(config)
