# PRJ7_NetPing_email_forwarder
https://netping.atlassian.net/wiki/spaces/PROJ/pages/1720778753/PRJ7+NetPIng+Email+forwarder

SMTP-прокси сервер для пересылки и переформатирования уведомлений по шаблону.

## start.py
Основной модуль. Проверяет структуры пользовательской и БД администратора и запускает остальные части сервиса.
Запуск:
```bash
python start.py --smtp_host <address> --smtp_port <port> --smtp_login <login> --smtp_pass <password> --user_db_host <address> --user_db_port <port> --user_db_username <username> --user_db_password <password> --user_db_name <dbname> --admin_db_host <address> --admin_db_port <port> --admin_db_username <username> --admin_db_password <password> --admin_db_name <dbname> --smtp2go_host <address> --smtp2go_port <port> --smtp2go_user <user> --smtp2go_pass <password> --web_host <address> --web_port <port> --log_dir <dir> --error_log_dir <dir>
```
, где

```--smtp_host <address>```, address - адрес, на котором smtp-сервер будет ожидать подключения, ip или имя;
```--smtp_port <port>```, port - порт, на котором smtp-сервер будет ожидать подключения, цифра;
```--smtp_login <login>```, login - имя пользователя для аутентификации пользователей(устройств), отправляющих письма;
```--smtp_pass <password>```, password - пароль для аутентификации пользователей(устройств), отправляющих письма.
```--user_db_host <address>```, address - адрес, на котором ожидает подключения сервер с пользовательской БД, ip или имя;
```--user_db_port <port>```, port - порт, на котором ожидает подключения сервер с пользовательской БД, ip или имя;
```--user_db_username <username>```, username - имя пользователя для подключения к пользовательской БД;
```--user_db_password <password>```, password - пароль для подключения к пользовательской БД;
```--user_db_name <dbname>```, dbname - название пользовательской БД;
```--admin_db_host <address>```, address - адрес, на котором ожидает подключения сервер с БД администратора, ip или имя;
```--admin_db_port <port>```, port - порт, на котором ожидает подключения сервер с БД администратора, ip или имя;
```--admin_db_username <username>```, username - имя пользователя для подключения к БД администратора;
```--admin_db_password <password>```, password - пароль для подключения к БД администратора;
```--admin_db_name <dbname>```, dbname - название БД администратора;
```--smtp2go_host <address>```, address - адрес сервиса SMTP2GO, ip или имя;
```--smtp2go_port <port>```, port - порт сервиса SMTP2GO, цифра;
```--smtp2go_user <user>```, user - пользователь для подключения к сервису SMTP2GO;
```--smtp2go_pass <password>```, password - пароль для подключения к сервису SMTP2GO.
```--web_host <address>```, address - адрес, на котором web-сервер будет ожидать подключения, ip или имя;
```--web_port <port>```, port - порт, на котором web-сервер будет ожидать подключения, цифра;
```--log_dir <dir>```, dir - каталог хранения лога logs.txt;
```--error_log_dir <dir>```, dir - каталог хранения лога errors.txt.

Ручной запуск остальных модулей обычно не требуется.

## smtp.py
SMTP-сервер. Принимает запросы от клиентов, аутентифицирует, принимает письма и добавляет их в очередь для дальнейшей обработки.
```bash
python smtp.py --smtp_host <address> --smtp_port <port> --smtp_login <login> --smtp_pass <password> --user_db_host <address> --user_db_port <port> --user_db_username <username> --user_db_password <password> --user_db_name <dbname> --log_dir <dir> --error_log_dir <dir>
```
, где

```--smtp_host <address>```, address - адрес, на котором smtp-сервер будет ожидать подключения, ip или имя;
```--smtp_port <port>```, port - порт, на котором smtp-сервер будет ожидать подключения, цифра;
```--smtp_login <login>```, login - имя пользователя для аутентификации пользователей(устройств), отправляющих письма;
```--smtp_pass <password>```, password - пароль для аутентификации пользователей(устройств), отправляющих письма.
```--user_db_host <address>```, address - адрес, на котором ожидает подключения сервер с пользовательской БД, ip или имя;
```--user_db_port <port>```, port - порт, на котором ожидает подключения сервер с пользовательской БД, ip или имя;
```--user_db_username <username>```, username - имя пользователя для подключения к пользовательской БД;
```--user_db_password <password>```, password - пароль для подключения к пользовательской БД;
```--user_db_name <dbname>```, dbname - название пользовательской БД;
```--log_dir <dir>```, dir - каталог хранения лога logs.txt;
```--error_log_dir <dir>```, dir - каталог хранения лога errors.txt.

## tasks.py
Модуль обработки писем. Извлекает из полученных писем данные, вставляет их в шаблоны и рассылает получателям.
Запуск:
```bash
python start.py --user_db_host <address> --user_db_port <port> --user_db_username <username> --user_db_password <password> --user_db_name <dbname> --admin_db_host <address> --admin_db_port <port> --admin_db_username <username> --admin_db_password <password> --admin_db_name <dbname> --smtp2go_host <address> --smtp2go_port <port> --smtp2go_user <user> --smtp2go_pass <password> --log_dir <dir> --error_log_dir <dir>
```
, где

```--user_db_host <address>```, address - адрес, на котором ожидает подключения сервер с пользовательской БД, ip или имя;
```--user_db_port <port>```, port - порт, на котором ожидает подключения сервер с пользовательской БД, ip или имя;
```--user_db_username <username>```, username - имя пользователя для подключения к пользовательской БД;
```--user_db_password <password>```, password - пароль для подключения к пользовательской БД;
```--user_db_name <dbname>```, dbname - название пользовательской БД;
```--admin_db_host <address>```, address - адрес, на котором ожидает подключения сервер с БД администратора, ip или имя;
```--admin_db_port <port>```, port - порт, на котором ожидает подключения сервер с БД администратора, ip или имя;
```--admin_db_username <username>```, username - имя пользователя для подключения к БД администратора;
```--admin_db_password <password>```, password - пароль для подключения к БД администратора;
```--admin_db_name <dbname>```, dbname - название БД администратора;
```--smtp2go_host <address>```, address - адрес сервиса SMTP2GO, ip или имя;
```--smtp2go_port <port>```, port - порт сервиса SMTP2GO, цифра;
```--smtp2go_user <user>```, user - пользователь для подключения к сервису SMTP2GO;
```--smtp2go_pass <password>```, password - пароль для подключения к сервису SMTP2GO.
```--log_dir <dir>```, dir - каталог хранения лога logs.txt;
```--error_log_dir <dir>```, dir - каталог хранения лога errors.txt.

## web.py
WEB-интерфейс для пользователей сервиса. Позволяет просматривать статистику и создавать/редактировать собственные шаблоны для уведомлений.
Запуск:
```bash
python start.py --user_db_host <address> --user_db_port <port> --user_db_username <username> --user_db_password <password> --user_db_name <dbname> --admin_db_host <address> --admin_db_port <port> --admin_db_username <username> --admin_db_password <password> --admin_db_name <dbname> --web_host <address> --web_port <port> --log_dir <dir> --error_log_dir <dir>
```
, где

```--user_db_host <address>```, address - адрес, на котором ожидает подключения сервер с пользовательской БД, ip или имя;
```--user_db_port <port>```, port - порт, на котором ожидает подключения сервер с пользовательской БД, ip или имя;
```--user_db_username <username>```, username - имя пользователя для подключения к пользовательской БД;
```--user_db_password <password>```, password - пароль для подключения к пользовательской БД;
```--user_db_name <dbname>```, dbname - название пользовательской БД;
```--admin_db_host <address>```, address - адрес, на котором ожидает подключения сервер с БД администратора, ip или имя;
```--admin_db_port <port>```, port - порт, на котором ожидает подключения сервер с БД администратора, ip или имя;
```--admin_db_username <username>```, username - имя пользователя для подключения к БД администратора;
```--admin_db_password <password>```, password - пароль для подключения к БД администратора;
```--admin_db_name <dbname>```, dbname - название БД администратора;
```--web_host <address>```, address - адрес, на котором web-сервер будет ожидать подключения, ip или имя;
```--web_port <port>```, port - порт, на котором web-сервер будет ожидать подключения, цифра;
```--log_dir <dir>```, dir - каталог хранения лога logs.txt;
```--error_log_dir <dir>```, dir - каталог хранения лога errors.txt.