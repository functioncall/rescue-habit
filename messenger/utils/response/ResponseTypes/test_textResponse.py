import unittest
from TextResponse import TextResponse

test_variables = {
    "test_eval_input": ["{{ someone }} had a little {{ something }}"],
    "test_eval_template_val": [{"someone": "Mary", "something": "lamb"}],
    "test_eval_output": ["Mary had a little lamb"]
}
textResponse = TextResponse(test_variables["test_eval_input"])


class TestTextResponse(unittest.TestCase):
    def test_eval(self):
        self.assertEqual(
            textResponse.eval(test_variables["test_eval_template_val"]),
            test_variables["test_eval_output"],
            "Expected output doesn't match the actual output."
        )

if __name__ == "__main__":
    unittest.main()