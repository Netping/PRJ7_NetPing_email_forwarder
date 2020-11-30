"""
DB connection module
"""
import typing

import psycopg2
import psycopg2.extras


schemas = {
    # Схема БД администратора
    'admin': [
        # Таблица шаблонов для разбора входящих писем
        '''
        create table if not exists inbound_templates
            (
                id serial primary key,
                name text not null,
                template text not null
            );
        ''',

        # Таблица шаблонов для отправки исходящих писем
        '''
        create table if not exists outbound_templates
            (
                id serial primary key,
                name text not null,
                template text not null,
                inbound_template_id integer not null,
                CONSTRAINT one_outbound_template UNIQUE(inbound_template_id)
            );
        '''
    ],

    # Схема пользовательской БД
    'user': [
        # Таблица шаблонов для отправки исходящих писем
        '''
        create table if not exists outbound_templates
            (
                id serial primary key,
                user text not null,
                name text not null,
                template text not null,
                inbound_template_id integer not null,
                CONSTRAINT one_outbound_template UNIQUE(user, inbound_template_id)
            );
        ''',

        # Таблица полученных писем
        '''
        create table if not exists mails
            (
                id serial primary key,
                receive_date timestamp with time zone not null,
                sender text not null,
                receive_meta json not null,
                data json,
                body text,
                inbound_template_id integer,
                send_meta json,
                send_date timestamp with time zone
            );
        '''
    ]
}


class DB:
    """
    Class for work with DB.

    Args
        - host -- DB host address
        - port -- DB host port
        - username -- username for connect to DB server
        - password -- password for connect to DB server
        - dbname -- database name
    """
    def __init__(self, host: str, port: int, username: str, password: str,
                 dbname: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.dbname = dbname

    def connect(self) -> None:
        """
        Connect to database server
        """
        self.connection = psycopg2.connect(host=self.host, port=self.port,
                                           user=self.username,
                                           password=self.password,
                                           dbname=self.dbname)

    def cursor(self):
        """
        Create cursor for execute queries
        """
        if not hasattr(self, 'connection') or not self.connection:
            raise Exception('Нет подключения к БД')
        return self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)

    def execute(self, sql, args=()) -> typing.List[typing.Dict]:
        """
        Execute query

        Args
            - sql -- SQL-query, text
            - args -- arguments to be insert into query
        """
        with self.cursor() as cursor:
            res = cursor.execute(sql, args)
            return res.fetchall()

    def check_structure(self, dbtype) -> None:
        """
        Check structure and create tables, sequencies and other if need it.

        Args:
            - dbtype -- Type of db: 'user' or 'admin'
        """
        schema = schemas.get(dbtype, None)
        if not schema:
            raise Exception('Неверно определен тип схемы БД')
        for sql in schema:
            self.execute(sql)


def create_db(host: str, port: int, username: str, password: str, dbname: str):
    db = DB(host, port, username, password, dbname)
    db.connect()
    return db
