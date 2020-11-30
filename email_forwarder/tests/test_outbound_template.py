import unittest

from email_forwarder.templates.outbound_template import OutboundTemplate


class TestOutboundTemplate(unittest.TestCase):
    def test_html(self):
        test_template = '''
<html>
    <head></head>
    <body>
        <p>Значение #1: {{value_1}}</p>
        <p>Значение #2: {{value_2}}</p>
        <p>Значение #3: {{value_3}}</p>
    </body>
</html>
        '''
        test_html = '''
<html>
    <head></head>
    <body>
        <p>Значение #1: 123</p>
        <p>Значение #2: 456</p>
        <p>Значение #3: 789</p>
    </body>
</html>
        '''
        values = {
            'value_1': '123',
            'value_2': '456',
            'value_3': '789',
        }
        template = OutboundTemplate(1, 1, 'Template #1', test_template, None)
        html = template.html(values)
        assert html == test_html, (f'Ожидаемый html:\n{test_html}\n'
                                   f'Полученный:\n{html}')

    def test_html_previous_mails(self):
        test_template = '''
<html>
    <head></head>
    <body>
        <p>Значение #1: {{value_1}}</p>
        <p>Значение #2: {{value_2}}</p>
        <p>Значение #3: {{value_3}}</p>
        {%- for mail in mails %}
            <div>
                <p>Значение #1: {{mail.value_1}}</p>
                <p>Значение #2: {{mail.value_2}}</p>
                <p>Значение #3: {{mail.value_3}}</p>
            </div>
        {%- endfor %}
    </body>
</html>
        '''
        test_html = '''
<html>
    <head></head>
    <body>
        <p>Значение #1: 123</p>
        <p>Значение #2: 456</p>
        <p>Значение #3: 789</p>
            <div>
                <p>Значение #1: 123</p>
                <p>Значение #2: 456</p>
                <p>Значение #3: 789</p>
            </div>
            <div>
                <p>Значение #1: 234</p>
                <p>Значение #2: 567</p>
                <p>Значение #3: 891</p>
            </div>
    </body>
</html>
        '''
        values = {
            'value_1': '123',
            'value_2': '456',
            'value_3': '789',
            'mails': [
                {
                    'value_1': '123',
                    'value_2': '456',
                    'value_3': '789',
                },
                {
                    'value_1': '234',
                    'value_2': '567',
                    'value_3': '891',
                }
            ]
        }
        template = OutboundTemplate(1, 1, 'Template #1', test_template, None)
        html = template.html(values)
        assert html == test_html, (f'Ожидаемый html:\n{test_html}\n'
                                   f'Полученный:\n{html}')
