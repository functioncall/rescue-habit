"""
    This class handles:

    1. Conversion of quick replies' template-strings to <Template>.
    2. Evaluating actual value of the strings from <template> using .eval()

    ======================================================
    QUICK_REPLIES: <list dict>
    template example:
        "quick_replies": {
          "iterable": {
            "type": "text",
            "title": "{{item_name}}",
            "payload": "{{item_tag}}"
          }
        }

    expected return value:
        [{
            "item_name": "Torch",
            "item_tag": "TORCH1NSB11"
        }, {
            "item_name": "Screwdriver",
            "item_tag": "SCREW1NSD13"
        }, ... ]

    ======================================================"""


from messenger.utils.response.ResponseTypes.Template import Template


class QuickReplyResponse(object):
    """
    Converts quick replies template-strings <list>  to <Template>
    """

    def __init__(self, quick_replies):
        """
        Converts Quick replies in template strings to <Template>
        :param quick_replies: <list dict>
        """
        self.quickRepliesInput      = quick_replies
        self.quickRepliesTemplate   = quick_replies
        self.quickRepliesTemplate   = self.templatize_quick_reply
        self.quickReplies           = []

    @property
    def templatize_quick_reply(self):
        if "iterable" in self.quickRepliesTemplate:
            for prop in self.quickRepliesTemplate["iterable"]:
                self.quickRepliesTemplate["iterable"][prop] = Template(self.quickRepliesTemplate["iterable"][prop])
        return self.quickRepliesTemplate

    def template_if_none(self, prop, doc):
        # if template is evaluated to be NoneType, return template-string as is.
        template_eval = self.quickRepliesTemplate["iterable"][prop].out(doc)

        return template_eval \
            if template_eval is not None \
            else self.quickRepliesTemplate["iterable"][prop].template

    def eval(self, collection=None):
        if collection is None:
            return self.quickReplies
        collection = collection if collection is not None else []           # type fallback

        if len(collection) == 0:
            return self.quickRepliesInput

        for doc in collection:                                              # get value from each object in collection
            self.quickReplies.append({                                      # set the props in template to value
                prop: self.template_if_none(prop, doc)                      # create output with template replaced with
                for prop in self.quickRepliesTemplate["iterable"]           # actual values
            })

        if "static" in self.quickRepliesTemplate:
            self.quickReplies.extend(self.quickRepliesTemplate["static"])

        result = self.quickReplies
        self.quickReplies = []
        return result
