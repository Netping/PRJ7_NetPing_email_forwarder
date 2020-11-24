from config import VERSION, get_parser, get_loggers


if __name__ == '__main__':
    config = get_parser(f'NetPIng Email forwarder v.{VERSION}, SMTP-Proxy server.',
                        ('user_db', 'smtp')).parse_args()
    log, error_log = get_loggers(config.log_dir, config.error_log_dir, 'smtp.py')
    log.info(f'NetPIng Email forwarder v.{VERSION}, SMTP-Proxy server.')

    user_db = create_db(config.user_db_host, config.user_db_port,
                        config.user_db_username, config.user_db_password,
                        config.user_db_name)
