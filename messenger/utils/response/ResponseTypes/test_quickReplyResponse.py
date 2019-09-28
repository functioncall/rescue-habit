import unittest
from Template import Template
from QuickReplyResponse import QuickReplyResponse


quickReplyResponse = QuickReplyResponse({
      "iterable": {
        "content_type": "text",
        "title": "{{category_name}}",
        "payload": "PREFERENCE_CATEGORY/{{category_tag}}"
      }
    })

validation_set = {
    "template_values": [{
        "category_name": "Potato",
        "category_tag": "VEGETABLE"
    }, {
        "category_name": "Carrot",
        "category_tag": "VEGETABLE"
    }],
    "expected_eval_output": [{
        "content_type": "text",
        "title": "Potato",
        "payload": "PREFERENCE_CATEGORY/VEGETABLE"
    }, {
        "content_type": "text",
        "title": "Carrot",
        "payload": "PREFERENCE_CATEGORY/VEGETABLE"
    }]
}

class TestQuickReplyResponse(unittest.TestCase):
    def test_templatize_quick_reply(self):
        fail_flg = False
        iterable = quickReplyResponse.quickRepliesTemplate["iterable"]
        for prop in iterable:
            if not isinstance(iterable[prop], Template):
                fail_flg = True
                break
        self.assertEqual(fail_flg, False, "Element in iterable is not an instance of Template class")

    def test_eval(self):
        template_output = quickReplyResponse.eval(validation_set["template_values"])
        self.assertEqual(
            str(template_output),
            str(validation_set["expected_eval_output"]),
            "Expected output doesn't match expected input"
        )

if __name__ == "__main__":
    unittest.main()