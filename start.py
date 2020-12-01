from multiprocessing import Process

from smtp import run_smtp_proxy
from tasks import run_tasks
from web import run_web
from email_forwarder.db import create_db
from email_forwarder.config import VERSION, get_parser, get_loggers


def run(config):
    log, error_log = get_loggers(config.log_dir, config.error_log_dir,
                                 'start.py')
    log.info(f'Start NetPIng Email forwarder v.{VERSION}.')

    admin_db = create_db(config.admin_db_host, config.admin_db_port,
                         config.admin_db_username, config.admin_db_password,
                         config.admin_db_name)
    admin_db.check_structure('admin')
    admin_db.close()

    user_db = create_db(config.user_db_host, config.user_db_port,
                        config.user_db_username, config.user_db_password,
                        config.user_db_name)
    user_db.check_structure('user')
    user_db.close()

    procs = list()
    smtp_proxy_proc = Process(target=run_smtp_proxy, args=(config,))
    procs.append(smtp_proxy_proc)
    smtp_proxy_proc.start()

    # tasks_proc = Process(target=run_tasks, args=(config,))
    # procs.append(tasks_proc)
    # tasks_proc.start()

    # web_proc = Process(target=run_web, args=(config,))
    # procs.append(web_proc)
    # web_proc.start()

    for proc in procs:
        proc.join()


if __name__ == '__main__':
    config = get_parser(f'NetPIng Email forwarder v.{VERSION}.').parse_args()
    run(config)
