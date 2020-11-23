"""
Module service configuration

Contains current version and functions for parse CLI arguments.
"""
import argparse


VERSION = '0'

def get_parser(description, enable_options=('user_db', 'admin_db', 'smtp', 'smtp2go', 'web')) -> argparse.ArgumentParser:
    """
        Args
            - description -- A description of what the program does
            - enable_options -- List of option whom adds to parser

        Return
            argparse.ArgumentParser object for extract arguments from CLI
    """
    parser = argparse.ArgumentParser(description=description)

    options = (
        ('user_db', add_user_db),
        ('admin_db', add_admin_db),
        ('smtp', add_smtp),
        ('smtp2go', add_smtp2go),
        ('web', add_web),
    )

    for opt in options:
        if opt[0] in enable_options:
            opt[1](parser)

    add_logs(parser)
    return parser

def add_user_db(parser: argparse.ArgumentParser) -> None:
    """
        Add user DB arguments into parser

        Args:
            - parser -- object argparse.ArgumentParser, in which add new arguments.
    """
    parser.add_argument('--user_db_host', required=True, type=str,
                        help=('User DB host, name or ip. '
                              'Example, --user_db_host 127.0.0.1, for local PostgreSQL server.'))
    parser.add_argument('--user_db_port', required=True, type=int,
                        help=('User DB port. Example, --user_db_port 5432'))
    parser.add_argument('--user_db_username', required=True, type=str,
                        help=('User DB username. Example, --user_db_username postgres'))
    parser.add_argument('--user_db_password', required=True, type=str,
                        help=('User DB password. Example, --user_db_password qwerty'))
    parser.add_argument('--user_db_name', required=True, type=str,
                        help=('User DB name. Example, --user_db_name database'))

def add_admin_db(parser: argparse.ArgumentParser) -> None:
    """
        Add admin DB arguments into parser

        Args:
            - parser -- object argparse.ArgumentParser, in which add new arguments.
    """
    parser.add_argument('--admin_db_host', required=True, type=str,
                        help=('Admin DB host, name or ip. '
                              'Example, --admin_db_host 127.0.0.1, for local PostgreSQL server.'))
    parser.add_argument('--admin_db_port', required=True, type=int,
                        help=('Admin DB port. Example, --admin_db_port 5432'))
    parser.add_argument('--admin_db_username', required=True, type=str,
                        help=('Admin DB username. Example, --admin_db_username postgres'))
    parser.add_argument('--admin_db_password', required=True, type=str,
                        help=('Admin DB password. Example, --admin_db_password qwerty'))
    parser.add_argument('--admin_db_name', required=True, type=str,
                        help=('Admin DB name. Example, --admin_db_name database'))

def add_smtp(parser: argparse.ArgumentParser) -> None:
    """
        Add SMTP arguments into parser

        Args:
            - parser -- object argparse.ArgumentParser, in which add new arguments.
    """
    parser.add_argument('--smtp_host', required=True, type=str,
                        help=('SMTP-server address to bind to. '
                              'Pass 0.0.0.0 to listens on all interfaces including '
                              'the external one. Example, --smtp_host 0.0.0.0'))
    parser.add_argument('--smtp_port', required=True, type=int,
                        help=('SMTP-server port to bind to. '
                              'Values below 1024 require root privileges. '
                              'Example, --smtp_port 8431'))
    parser.add_argument('--smtp_login', required=True, type=str,
                        help=('SMTP-server login for authentificate users. '
                              'Example, --smtp_login user'))
    parser.add_argument('--smtp_pass', required=True, type=str,
                        help=('SMTP-server password for authentificate users.'))

def add_smtp2go(parser: argparse.ArgumentParser) -> None:
    """
        Add SMTP2GO service arguments into parser

        Args:
            - parser -- object argparse.ArgumentParser, in which add new arguments.
    """
    parser.add_argument('--smtp2go_host', required=True, type=str,
                        help=('SMTP2GO address. Example, --smtp2go_host mail.smtp2go.com'))
    parser.add_argument('--smtp2go_port', required=True, type=int,
                        help=('SMTP2GO port. Example, --smtp2go_port 2525'))
    parser.add_argument('--smtp2go_user', required=True, type=str,
                        help=('SMTP2GO username. Example, --smtp2go_user username'))
    parser.add_argument('--smtp2go_pass', required=True, type=str,
                        help=('SMTP2GO username. Example, --smtp2go_pass password'))

def add_web(parser: argparse.ArgumentParser) -> None:
    """
        Add WEB arguments into parser

        Args:
            - parser -- object argparse.ArgumentParser, in which add new arguments.
    """
    parser.add_argument('--web_host', required=True, type=str,
                        help=('WEB-server address to bind to. '
                              'Pass 0.0.0.0 to listens on all interfaces including '
                              'the external one. Example, --web_host 0.0.0.0'))
    parser.add_argument('--web_port', required=True, type=int,
                        help=('WEB-server port to bind to. '
                              'Values below 1024 require root privileges. '
                              'Example, --web_port 8431'))

def add_logs(parser: argparse.ArgumentParser) -> None:
    """
        Add logs arguments into parser

        Args:
            - parser -- object argparse.ArgumentParser, in which add new arguments.
    """
    parser.add_argument('--log_dir', required=True, type=str,
                        help=('Dir for log.txt. Example for current dir, .'))
    parser.add_argument('--error_log_dir', required=True, type=str,
                        help=('Dir for errors.txt. Example for current dir, .'))
