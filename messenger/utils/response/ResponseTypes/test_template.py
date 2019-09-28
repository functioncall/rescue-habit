import unittest
from Template import Template

template_str = "{{ some_variable }}"
template = Template(template_str)
validation_set = {
    "variables": ["{{some_variable}}"],
    "test_out_input": ["this is a test"],
    "test_out_output": "this is a test"
}


class TestTemplate(unittest.TestCase):
    def test_clean_template(self):
        template.clean_template()
        self.assertEqual(template.variables, validation_set["variables"], "Failed to extract variables from template_str")

    def test_out(self):
        self.assertEqual(template.out(validation_set["test_out_input"]), validation_set["test_out_output"], "Output doesn't match the expected output.")


if __name__ == "__main__":
    unittest.main()