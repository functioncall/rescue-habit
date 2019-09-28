"""
    This class handles

    1. Conversion of attachments' template-strings to <Template>.
    2. Evaluating actual value of the strings from <template> using .eval()

    example:
        ATTACHMENTS: <dict>
        template example:
            "attachments": {
              "iterable": {
                "type": "template",
                "elements": {
                  "title": "{{product_name}}",
                  "image": "{{image_url}}",
                  "buttons": [{
                      "title": "Add {{product_name}} to cart",
                      "type": "text",
                      "payload": "CART_IN?p_id={{product_id}}"
                    },
                    {
                      "title": "Remove {{product_name}} from cart",
                      "type": "text",
                      "payload": "CART_OUT?p_id={{product_id}}"
                    }]
                }
              }
            }

        expected return value: {
            "type": "template",
            "elements: [{
                "product_name": "Torch",
                "image_url": "404 Not Found",
                "buttons": [{
                    "product_name": "Torch",
                    "product_id": "TORCH1NSB11"
                }, {
                    "product_name": "Torch",
                    "product_id": "TORCH1NSB11"
                }]
            }]
        }
"""

from messenger.utils.response.ResponseTypes.Template import Template
from commons.logger import log

class AttachmentResponse(object):
    """
    Converts attachment <dict> template-strings to <Template>
    """
    def __init__(self, attachments):
        """
        :param attachments: <dict>
        attachmentsTemplate: <Template>
        attachments = <dict> (obtained after running eval)
        """
    
        self.attachmentsInput = attachments
        self.attachmentsTemplate = attachments
        self.attachmentsTemplate = self.templatize_attachments
        self.attachments = {
          "type": "template",
          "payload": {
              "elements": {
                  "buttons": []
              }
          }
        }

    @property
    def templatize_attachments(self):
        if type(self.attachmentsTemplate["payload"]["elements"]) is dict:
            self.attachmentsTemplate["type"] = Template(self.attachmentsTemplate["type"])
            self.attachmentsTemplate["payload"]["template_type"] = Template(
                self.attachmentsTemplate["payload"]["template_type"]
            )
            self.attachmentsTemplate["payload"]["elements"]["title"] = Template(self.attachmentsTemplate["payload"]["elements"]["title"])
        else:
            return self.attachmentsInput

        if "image_url" in self.attachmentsTemplate["payload"]["elements"]:
            self.attachmentsTemplate["payload"]["elements"]["image_url"] = \
                Template(self.attachmentsTemplate["payload"]["elements"]["image_url"])

        if "subtitle" in self.attachmentsTemplate["payload"]["elements"]:
            self.attachmentsTemplate["payload"]["elements"]["subtitle"] = \
                Template(self.attachmentsTemplate["payload"]["elements"]["subtitle"])

        for i, button in enumerate(
                self.attachmentsTemplate["payload"]["elements"]["buttons"]
        ):
            for prop in button:
                button[prop] = Template(button[prop])
            self.attachmentsTemplate["payload"]["elements"]["buttons"][i] = button
        return self.attachmentsTemplate

    def eval(self, doc):
        """
        :param doc: <dict> containing values for attachment
        :return: <dict> templates -> str, using values in doc
        """
        print('-' * 100)
        print(doc)
        print('-' * 100)
        if doc is None:
            return self.attachmentsInput
        self.attachments["type"] = self.attachmentsTemplate["type"].out({})
        self.attachments["payload"]["template_type"] = self.attachmentsTemplate["payload"]["template_type"].out({})
        self.attachments["payload"]["elements"] = []
        for el in doc:
            element = {
              "title": self.attachmentsTemplate["payload"]["elements"]["title"].out(el),
              "buttons": [],
            }

            if "image_url" in self.attachmentsTemplate["payload"]["elements"]:
                element["image_url"] = self.attachmentsTemplate["payload"]["elements"]["image_url"].out(el)
            if "subtitle" in self.attachmentsTemplate["payload"]["elements"]:
                element["subtitle"] = self.attachmentsTemplate["payload"]["elements"]["subtitle"].out(el)




            for i, button_props in enumerate(self.attachmentsTemplate["payload"]["elements"]["buttons"]):
                element["buttons"].append({
                    prop: button_props[prop].out(el["buttons"][i]) for prop in button_props
                })
            self.attachments["payload"]["elements"].append(element)

        result = self.attachments
        self.attachments = {
          "type": "template",
          "payload": {}
        }
        return result
