import typing
import re


class InboundTemplate:
    def __init__(self, template_id: int, name: str, template: str):
        self.template_id = template_id
        self.name = name
        self.template = template

    def parse(self, text: str) -> typing.Optional[dict]:
        """
        Parse text with current template.

        Args:
            - text -- text for parsing

        Return optional dict
        """
        values = re.findall(r'{{\s*([\d\w]+)\s*}}', self.template)
        if not values:
            return None

        escaped_template = self.template.translate(str.maketrans({
            '(': r'\(',
            ')': r'\)',
            '#': r'\#',
            '%': r'\%',
            # '-': r'\-',
            '=': r'\=',
            '+': r'\+',
            '.': r'\.',
            ',': r'\,',
            '?': r'\?',
            '!': r'\!',
        }))

        field_template = r'{{\s*([\d\w]+)(\:([\w\d\s\+\%\\\-\_\.\|\s\"\']+))?\s*}}'
        group_template = r'(?P<\1>[\\w\\d\\s\\+\\%\\-\\_\\.]+)?'
        group_options_template = r'(?P<\1>\2)?'
        default_value_template = r'[\w\d\s\+\%\-\_\.]+'

        regex = re.sub(field_template,
                       lambda m: r'(?P<' + m.group(1) + '>' + (m.group(3) or default_value_template) + r')?', escaped_template)
        regex = re.sub(r'\[\[(.*)\]\]', r'(\1)?', regex)
        
        data = re.search(regex, text).groupdict()
        return data
