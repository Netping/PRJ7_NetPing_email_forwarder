from db import create_db
from config import VERSION, get_parser, get_loggers

def run(config):
    log, error_log = get_loggers(config.log_dir, config.error_log_dir, 'start.py')
    log.info(f'Start NetPIng Email forwarder v.{VERSION}.')
    
    admin_db = create_db(config.admin_db_host, config.admin_db_port,
                         config.admin_db_username, config.admin_db_password,
                         config.admin_db_name)
    admin_db.check_structure('admin')
    
    user_db = create_db(config.user_db_host, config.user_db_port,
                        config.user_db_username, config.user_db_password,
                        config.user_db_name)
    user_db.check_structure('user')


if __name__ == '__main__':
    config = get_parser(f'NetPIng Email forwarder v.{VERSION}.').parse_args()
    run(config)
