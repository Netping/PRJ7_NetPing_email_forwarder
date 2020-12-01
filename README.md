# PRJ7_NetPing_email_forwarder
https://netping.atlassian.net/wiki/spaces/PROJ/pages/1720778753/PRJ7+NetPIng+Email+forwarder

SMTP-прокси сервер для пересылки и переформатирования уведомлений по шаблону.

## Подготовка
Перед запуском необходимо установить все необходимые зависимости:
```bash
pip install -r requirements.txt
```
Зависимости
- Flask(требует Werkzeug и MarkupSafe), Jinja2 и waitress необходимы для web-сервера;
- Jinja2 также используется при подготовке писем для пересылки, гшаблоны для отправки;
- psycopg2-binary для подключения в PotgsreSQL. Выбор в пользу бинарной сборки, чтобы не доавлять зависимостей по наличию PostgreSQL на сервере/в контейнере.

## Изменения в схемах баз данных
После публикации первой версии все последующие изменения в текущих таблицах делать только через ```alter table```. В противном случае можно нарушить целостность и потерять часть или все данные.

## start.py
Основной модуль. Проверяет структуры пользовательской и БД администратора и запускает остальные части сервиса.
Запуск:
```bash
python start.py --smtp_host <address> --smtp_port <port> --smtp_login <login> --smtp_pass <password> --user_db_host <address> --user_db_port <port> --user_db_username <username> --user_db_password <password> --user_db_name <dbname> --admin_db_host <address> --admin_db_port <port> --admin_db_username <username> --admin_db_password <password> --admin_db_name <dbname> --smtp2go_host <address> --smtp2go_port <port> --smtp2go_user <user> --smtp2go_pass <password> --web_host <address> --web_port <port> --log_dir <dir> --error_log_dir <dir>
```
, где

- ```--smtp_host <address>```, address - адрес, на котором smtp-сервер будет ожидать подключения, ip или имя;
- ```--smtp_port <port>```, port - порт, на котором smtp-сервер будет ожидать подключения, цифра;
- ```--smtp_login <login>```, login - имя пользователя для аутентификации пользователей(устройств), отправляющих письма;
- ```--smtp_pass <password>```, password - пароль для аутентификации пользователей(устройств), отправляющих письма.
- ```--user_db_host <address>```, address - адрес, на котором ожидает подключения сервер с пользовательской БД, ip или имя;
- ```--user_db_port <port>```, port - порт, на котором ожидает подключения сервер с пользовательской БД, ip или имя;
- ```--user_db_username <username>```, username - имя пользователя для подключения к пользовательской БД;
- ```--user_db_password <password>```, password - пароль для подключения к пользовательской БД;
- ```--user_db_name <dbname>```, dbname - название пользовательской БД;
- ```--admin_db_host <address>```, address - адрес, на котором ожидает подключения сервер с БД администратора, ip или имя;
- ```--admin_db_port <port>```, port - порт, на котором ожидает подключения сервер с БД администратора, ip или имя;
- ```--admin_db_username <username>```, username - имя пользователя для подключения к БД администратора;
- ```--admin_db_password <password>```, password - пароль для подключения к БД администратора;
- ```--admin_db_name <dbname>```, dbname - название БД администратора;
- ```--smtp2go_host <address>```, address - адрес сервиса SMTP2GO, ip или имя;
- ```--smtp2go_port <port>```, port - порт сервиса SMTP2GO, цифра;
- ```--smtp2go_user <user>```, user - пользователь для подключения к сервису SMTP2GO;
- ```--smtp2go_pass <password>```, password - пароль для подключения к сервису SMTP2GO.
- ```--web_host <address>```, address - адрес, на котором web-сервер будет ожидать подключения, ip или имя;
- ```--web_port <port>```, port - порт, на котором web-сервер будет ожидать подключения, цифра;
- ```--log_dir <dir>```, dir - каталог хранения лога logs.txt;
- ```--error_log_dir <dir>```, dir - каталог хранения лога errors.txt.

Ручной запуск остальных модулей обычно не требуется.

## smtp.py
SMTP-сервер. Принимает запросы от клиентов, аутентифицирует, принимает письма и добавляет их в очередь для дальнейшей обработки.
```bash
python smtp.py --smtp_host <address> --smtp_port <port> --smtp_login <login> --smtp_pass <password> --user_db_host <address> --user_db_port <port> --user_db_username <username> --user_db_password <password> --user_db_name <dbname> --log_dir <dir> --error_log_dir <dir>
```
, где

- ```--smtp_host <address>```, address - адрес, на котором smtp-сервер будет ожидать подключения, ip или имя;
- ```--smtp_port <port>```, port - порт, на котором smtp-сервер будет ожидать подключения, цифра;
- ```--smtp_login <login>```, login - имя пользователя для аутентификации пользователей(устройств), отправляющих письма;
- ```--smtp_pass <password>```, password - пароль для аутентификации пользователей(устройств), отправляющих письма.
- ```--user_db_host <address>```, address - адрес, на котором ожидает подключения сервер с пользовательской БД, ip или имя;
- ```--user_db_port <port>```, port - порт, на котором ожидает подключения сервер с пользовательской БД, ip или имя;
- ```--user_db_username <username>```, username - имя пользователя для подключения к пользовательской БД;
- ```--user_db_password <password>```, password - пароль для подключения к пользовательской БД;
- ```--user_db_name <dbname>```, dbname - название пользовательской БД;
- ```--log_dir <dir>```, dir - каталог хранения лога logs.txt;
- ```--error_log_dir <dir>```, dir - каталог хранения лога errors.txt.

## tasks.py
Модуль обработки писем. Извлекает из полученных писем данные, вставляет их в шаблоны и рассылает получателям.
Запуск:
```bash
python start.py --user_db_host <address> --user_db_port <port> --user_db_username <username> --user_db_password <password> --user_db_name <dbname> --admin_db_host <address> --admin_db_port <port> --admin_db_username <username> --admin_db_password <password> --admin_db_name <dbname> --smtp2go_host <address> --smtp2go_port <port> --smtp2go_user <user> --smtp2go_pass <password> --log_dir <dir> --error_log_dir <dir>
```
, где

-  ```--user_db_host <address>```, address - адрес, на котором ожидает подключения сервер с пользовательской БД, ip или имя;
-  ```--user_db_port <port>```, port - порт, на котором ожидает подключения сервер с пользовательской БД, ip или имя;
-  ```--user_db_username <username>```, username - имя пользователя для подключения к пользовательской БД;
-  ```--user_db_password <password>```, password - пароль для подключения к пользовательской БД;
-  ```--user_db_name <dbname>```, dbname - название пользовательской БД;
-  ```--admin_db_host <address>```, address - адрес, на котором ожидает подключения сервер с БД администратора, ip или имя;
-  ```--admin_db_port <port>```, port - порт, на котором ожидает подключения сервер с БД администратора, ip или имя;
-  ```--admin_db_username <username>```, username - имя пользователя для подключения к БД администратора;
-  ```--admin_db_password <password>```, password - пароль для подключения к БД администратора;
-  ```--admin_db_name <dbname>```, dbname - название БД администратора;
-  ```--smtp2go_host <address>```, address - адрес сервиса SMTP2GO, ip или имя;
-  ```--smtp2go_port <port>```, port - порт сервиса SMTP2GO, цифра;
-  ```--smtp2go_user <user>```, user - пользователь для подключения к сервису SMTP2GO;
-  ```--smtp2go_pass <password>```, password - пароль для подключения к сервису SMTP2GO.
-  ```--log_dir <dir>```, dir - каталог хранения лога logs.txt;
-  ```--error_log_dir <dir>```, dir - каталог хранения лога errors.txt.

## web.py
WEB-интерфейс для пользователей сервиса. Позволяет просматривать статистику и создавать/редактировать собственные шаблоны для уведомлений.
Запуск:
```bash
python start.py --user_db_host <address> --user_db_port <port> --user_db_username <username> --user_db_password <password> --user_db_name <dbname> --admin_db_host <address> --admin_db_port <port> --admin_db_username <username> --admin_db_password <password> --admin_db_name <dbname> --web_host <address> --web_port <port> --log_dir <dir> --error_log_dir <dir>
```
, где

- ```--user_db_host <address>```, address - адрес, на котором ожидает подключения сервер с пользовательской БД, ip или имя;
- ```--user_db_port <port>```, port - порт, на котором ожидает подключения сервер с пользовательской БД, ip или имя;
- ```--user_db_username <username>```, username - имя пользователя для подключения к пользовательской БД;
- ```--user_db_password <password>```, password - пароль для подключения к пользовательской БД;
- ```--user_db_name <dbname>```, dbname - название пользовательской БД;
- ```--admin_db_host <address>```, address - адрес, на котором ожидает подключения сервер с БД администратора, ip или имя;
- ```--admin_db_port <port>```, port - порт, на котором ожидает подключения сервер с БД администратора, ip или имя;
- ```--admin_db_username <username>```, username - имя пользователя для подключения к БД администратора;
- ```--admin_db_password <password>```, password - пароль для подключения к БД администратора;
- ```--admin_db_name <dbname>```, dbname - название БД администратора;
- ```--web_host <address>```, address - адрес, на котором web-сервер будет ожидать подключения, ip или имя;
- ```--web_port <port>```, port - порт, на котором web-сервер будет ожидать подключения, цифра;
- ```--log_dir <dir>```, dir - каталог хранения лога logs.txt;
- ```--error_log_dir <dir>```, dir - каталог хранения лога errors.txt.

## Шаблоны для парсинга писем
Для извлечения неких данных из письма часть помечается часть текста - помещается в двойные фигурные скорбки. Пример,
```
{{ variable }}
```
Указанное в скобках является именем переменной(в данном случае ```variable```), по которой к ней можно обратиться в шаблоне исходящего письма.

Если часть текста является опциональной, она помещается в двойные квардратные скобки. Пример,
```
[[что-то]]
```
При этом, пробелы вокруг опционального текста лучше захватить в квадратные скобки.

Для ограничения возможного текста рядом вариантов, они указывается в фигурных скобках через двоеточие после имени переменной и разделяются вертикальной чертой:
```
{{ var:вариант 1|вариант 2 }}
```

Примеры:
```
Термо: кан.{{n}} "{{memo}}" {{t}}C, {{status}} ({{lnr}}..{{hnr}}C)

Термо: кан.{{n}} - {{message}}

Датчик влажности {{n}}[[ "{{memo}}"]] - температура {{t}}C ({{status}} {{lnr}}..{{hnr}}C)

PWR: реле {{n}} "{{memo}}" {{action:получило команду "Вкл"|получило команду "Выкл"|временно выключено на Nс|временно включено на Nс|включено|выключено|переведено в режим "управление по расписанию и от сторожа"|переведено в режим "управление по расписанию и от логики"}}[[ {{cmd_src:через веб-интерфейс|от логики|от расписания|от сторожа|вызовом cgi|через SNMP}}]]

Влажность {{h}}%, {{status}} ({{lnr}}..{{hnr}}%)

IO{{n}}={{lvl}} "{{memo}}"[[ {{legend}}]]

{{measurement}}: кан.{{n}} "{{memo}}" {{value}}, {{status}}
```

## Шаблоны исходящих писем
Исходящие письма формируются шабнолизатором Jinja2. Полную документацию можно найти на официалном сайте https://jinja.palletsprojects.com/en/2.11.x/.

## Модульные тесты
### Тестирование входящих шаблонов
```bash
python -m unittest email_forwarder/tests/test_inbound_template.py
```

### Тестирование исходящих шаблонов
```bash
python -m unittest email_forwarder/tests/test_outbound_template.py
```