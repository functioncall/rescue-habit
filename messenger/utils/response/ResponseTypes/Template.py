import re
from commons.logger import log


class Template(object):
    """
    Template class handles:
    1. one-to-one variable to value mapping.
    2. multi-value variables can be mapped via '...' convention.
    3. delimiters can be enabled as configurable in future.
    """

    def __init__(self, template_str):
        self.template = template_str
        self.delimiters = {"start": "{{", "end": "}}"}
        self.variables = None
        self.clean_template()

    def clean_template(self):
        """
        Remove empty spaces inside template pattern, and find variables.
        {{    abc    }} => {{abc}}
        :return: None
        """
        self.template = re.sub(r"(?<={{) *", '', self.template)
        self.template = re.sub(r" *(?=}})", '', self.template)
        self.variables = re.findall(r"{{[^}]+}}", self.template)

    def out(self, values):
        """
        :param values: dictionary of values for each variable.
        :return: string with values replacing the variables in the template.
        """
        result = self.template

        for value in values:

            key = self.delimiters["start"] + value + self.delimiters["end"]
            if key in self.variables and '...' in key:
                result = result.replace(key, ', '.join(values[value]))
            elif key in self.variables:
                result = result.replace(key, values[value])
        return result
