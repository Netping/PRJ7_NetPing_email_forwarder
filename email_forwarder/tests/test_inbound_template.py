import unittest

from templates.inbound_template import InboundTemplate


class TestInboundTemplate(unittest.TestCase):
    def test_parse_term_1(self):
        test_template = ('Термо: кан.{{n}} "{{memo}}" {{t}}C, '
                         '{{status}} ({{lnr}}..{{hnr}}C)')

        example_1 = 'Термо: кан.1 "memo" +29C, выше нормы (25..28C)'
        test_data_1 = {
            'n': '1',
            'memo': 'memo',
            't': '+29',
            'status': 'выше нормы',
            'lnr': '25',
            'hnr': '28',
        }

        example_2 = 'Термо: кан.1 "memo" +24C, ниже нормы (25..28C)'
        test_data_2 = {
            'n': '1',
            'memo': 'memo',
            't': '+24',
            'status': 'ниже нормы',
            'lnr': '25',
            'hnr': '28',
        }

        template = InboundTemplate(1, 'Template #1', test_template)
        data_1 = template.parse(example_1)
        data_2 = template.parse(example_2)
        assert test_data_1 == data_1, (f'Ожидаемые значения:\n{test_data_1}\n'
                                       f'Полученные:\n{data_1}')
        assert test_data_2 == data_2, (f'Ожидаемые значения:\n{test_data_2}\n'
                                       f'Полученные:\n{data_2}')

    def test_parse_term_2(self):
        test_template = ('Термо: кан.{{n}} - {{message}}')

        example = 'Термо: кан.1 - датчик отсутствует или неисправен'
        test_data = {
            'n': '1',
            'message': 'датчик отсутствует или неисправен',
        }

        template = InboundTemplate(1, 'Template #1', test_template)
        data = template.parse(example)
        assert test_data == data, (f'Ожидаемые значения:\n{test_data}\n'
                                   f'Полученные:\n{data}')

    def test_parse_term_humidity_1(self):
        test_template = ('Датчик влажности {{n}}[[ "{{memo}}"]] - температура '
                         '{{t}}C ({{status}} {{lnr}}..{{hnr}}C)')

        example = 'Датчик влажности 1 - температура 23C (ниже нормы 24..29C)'
        test_data = {
            'n': '1',
            'memo': None,
            't': '23',
            'status': 'ниже нормы',
            'lnr': '24',
            'hnr': '29',
        }

        template = InboundTemplate(1, 'Template #1', test_template)
        data = template.parse(example)
        assert test_data == data, (f'Ожидаемые значения:\n{test_data}\n'
                                   f'Полученные:\n{data}')

    def test_parse_term_releay(self):
        action_options = '|'.join([
            'получило команду "Вкл"',
            'получило команду "Выкл"',
            'временно выключено на Nс',
            'временно включено на Nс',
            'включено',
            'выключено',
            'переведено в режим "управление по расписанию и от сторожа"',
            'переведено в режим "управление по расписанию и от логики"',
        ])
        cmd_options = '|'.join([
            'через веб-интерфейс',
            'от логики',
            'от расписания',
            'от сторожа',
            'вызовом cgi',
            'через SNMP',
        ])
        test_template = ('PWR: реле {{n}} "{{memo}}" '
                         '{{action:%s}}[[ {{cmd_src:%s}}]]') % (
                             action_options, cmd_options
                         )

        example_1 = 'PWR: реле 1 "relay1" включено'
        test_data_1 = {
            'n': '1',
            'memo': 'relay1',
            'action': 'включено',
            'cmd_src': None
        }

        example_2 = ('PWR: реле 1 "relay1" переведено в режим "управление '
                     'по расписанию и от сторожа" через веб-интерфейс')
        test_data_2 = {
            'n': '1',
            'memo': 'relay1',
            'action': ('переведено в режим "управление по '
                       'расписанию и от сторожа"'),
            'cmd_src': 'через веб-интерфейс'
        }

        example_3 = ('PWR: реле 1 "relay1" переведено в режим "управление '
                     'по расписанию и от логики" через веб-интерфейс')
        test_data_3 = {
            'n': '1',
            'memo': 'relay1',
            'action': ('переведено в режим "управление по '
                       'расписанию и от логики"'),
            'cmd_src': 'через веб-интерфейс'
        }

        template = InboundTemplate(1, 'Template #1', test_template)
        data_1 = template.parse(example_1)
        data_2 = template.parse(example_2)
        data_3 = template.parse(example_3)
        assert test_data_1 == data_1, (f'Ожидаемые значения:\n{test_data_1}\n'
                                       f'Полученные:\n{data_1}')
        assert test_data_2 == data_2, (f'Ожидаемые значения:\n{test_data_2}\n'
                                       f'Полученные:\n{data_2}')
        assert test_data_3 == data_3, (f'Ожидаемые значения:\n{test_data_3}\n'
                                       f'Полученные:\n{data_3}')

    def test_parse_i2c(self):
        test_template = ('Влажность {{h}}%, {{status}} ({{lnr}}..{{hnr}}%)')

        example_1 = 'Влажность 80%, в пределах нормы (40..85%)'
        test_data_1 = {
            'h': '80',
            'status': 'в пределах нормы',
            'lnr': '40',
            'hnr': '85',
        }

        example_2 = 'Влажность 38%, ниже нормы (40..85%)'
        test_data_2 = {
            'h': '38',
            'status': 'ниже нормы',
            'lnr': '40',
            'hnr': '85',
        }

        template = InboundTemplate(1, 'Template #1', test_template)
        data_1 = template.parse(example_1)
        data_2 = template.parse(example_2)
        assert test_data_1 == data_1, (f'Ожидаемые значения:\n{test_data_1}\n'
                                       f'Полученные:\n{data_1}')
        assert test_data_2 == data_2, (f'Ожидаемые значения:\n{test_data_2}\n'
                                       f'Полученные:\n{data_2}')

    def test_parse_io(self):
        test_template = 'IO{{n}}={{lvl}} "{{memo}}"[[ {{legend}}]]'

        example_1 = 'IO1=1 "Линия1" лог1'
        test_data_1 = {
            'n': '1',
            'lvl': '1',
            'memo': 'Линия1',
            'legend': 'лог1',
        }

        example_1 = 'IO1=1 "Линия1"'
        test_data_1 = {
            'n': '1',
            'lvl': '1',
            'memo': 'Линия1',
            'legend': None,
        }

        template = InboundTemplate(1, 'Template #1', test_template)
        data_1 = template.parse(example_1)
        assert test_data_1 == data_1, (f'Ожидаемые значения:\n{test_data_1}\n'
                                       f'Полученные:\n{data_1}')

    def test_parse_voltage(self):
        test_template = ('{{measurement}}: кан.{{n}} "{{memo}}" '
                         '{{value}}, {{status}}')

        examples = (
            (
                'Напряжение: кан.1 "12321321" 0В, Отказ',
                {
                    'measurement': 'Напряжение',
                    'n': '1',
                    'memo': '12321321',
                    'value': '0В',
                    'status': 'Отказ',
                }
            ),
            (
                'Напряжение: кан.1 "12321321" 18В, Нет напряжения',
                {
                    'measurement': 'Напряжение',
                    'n': '1',
                    'memo': '12321321',
                    'value': '18В',
                    'status': 'Нет напряжения',
                }
            ),
            (
                'Импульс напряжения: кан.1 "12321321" 33В, Отсутствуют',
                {
                    'measurement': 'Импульс напряжения',
                    'n': '1',
                    'memo': '12321321',
                    'value': '33В',
                    'status': 'Отсутствуют',
                }
            ),
            (
                'Провал напряжения: кан.1 "12321321" 0В, Отсутствуют',
                {
                    'measurement': 'Провал напряжения',
                    'n': '1',
                    'memo': '12321321',
                    'value': '0В',
                    'status': 'Отсутствуют',
                }
            ),
            (
                'Частота: кан.1 "12321321" 50.00Гц, Отлично',
                {
                    'measurement': 'Частота',
                    'n': '1',
                    'memo': '12321321',
                    'value': '50.00Гц',
                    'status': 'Отлично',
                }
            ),
            (
                'Напряжение: кан.1 "12321321" 23В, Плохо',
                {
                    'measurement': 'Напряжение',
                    'n': '1',
                    'memo': '12321321',
                    'value': '23В',
                    'status': 'Плохо',
                }
            ),
            (
                'Провал напряжения: кан.1 "12321321" 94В, Небольшие',
                {
                    'measurement': 'Провал напряжения',
                    'n': '1',
                    'memo': '12321321',
                    'value': '94В',
                    'status': 'Небольшие',
                }
            ),
            (
                'Частота: кан.1 "12321321" 49.98Гц, Отлично',
                {
                    'measurement': 'Частота',
                    'n': '1',
                    'memo': '12321321',
                    'value': '49.98Гц',
                    'status': 'Отлично',
                }
            ),
            (
                'Провал напряжения: кан.1 "12321321" 5В, Отсутствуют',
                {
                    'measurement': 'Провал напряжения',
                    'n': '1',
                    'memo': '12321321',
                    'value': '5В',
                    'status': 'Отсутствуют',
                }
            ),
        )

        template = InboundTemplate(1, 'Template #1', test_template)
        for example in examples:
            test_data = template.parse(example[0])
            assert test_data == example[1], (
                f'Ожидаемые значения:\n{test_data}\nПолученные:\n{example[1]}')
