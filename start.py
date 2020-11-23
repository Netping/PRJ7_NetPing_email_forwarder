from config import VERSION, get_parser, get_loggers


if __name__ == '__main__':
    config = get_parser(f'NetPIng Email forwarder v.{VERSION}.').parse_args()
    log, error_log = get_loggers(config.log_dir, config.error_log_dir, 'start.py')
    log.info(f'Start NetPIng Email forwarder v.{VERSION}.')
