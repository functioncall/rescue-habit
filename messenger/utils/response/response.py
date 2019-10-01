import json
import os
import random

import requests
from django_project import settings
from django.http import HttpResponse, JsonResponse

from messenger.utils.response.ResponseTypes.QuickReplyResponse import QuickReplyResponse
from messenger.utils.response.ResponseTypes.TextResponse import TextResponse
from django.conf import settings


def value_validator(variables, values):
    """
    1. Checks if "values" is of type <dict>
    2. Checks if all variables are present in the values <dict>
    :param variables: <list>
    :param values: <dict>
    :raise: InvalidTemplateValues, IncompleteTemplateValues
    :return None
    """
    return None
    # if type(values) is not dict:
    #     raise InvalidTemplateValues(values)
    # elif set(variables) != set(dict.keys(values)):
    #     raise IncompleteTemplateValues([v for v in variables if v not in values])


class Response(object):
    """
    Response class for chat data and text templating.
    """

    def __init__(self, data, page_access_token=None):
        """
        :param data: message data
        """
        self.params = {"access_token": page_access_token}
        self.headers = {"Content-Type": "application/json"}
        self.data = {"recipient": {"id": None}, "message": {}}

        self.text = TextResponse(data["text"]) \
            if "text" in data else None
        self.quick_replies = QuickReplyResponse(data["quick_replies"]) \
            if "quick_replies" in data else None

        self.attachments = data.get("attachments", {})

    def add_recipient_id(self, recipient_id):
        """
        Adds the chat receivers id to instance
        :param recipient_id: facebook_id of a chat participant
        """
        self.data["recipient"]["id"] = recipient_id

    def send_to(self, recipient_id, page_access_token, node_name):
        """
        Orders messages before sending
        :param recipient_id: facebook_id of a chat participant
        """
        self.params = {"access_token": page_access_token}
        self.add_recipient_id(recipient_id)
        r = None

        if self.quick_replies and self.text:                        # If quick_replies and text
            r = self.send(self.data["message"], ["quick_replies", "text"], recipient_id)    # are both present send both

        elif self.text:
            # send text if quick_replies
            r = self.send(self.data["message"], ["text"], recipient_id)                     # are not present

        if self.attachments:                                                    # Send attachments alone
            r = self.send(self.data["message"], ["attachment"], recipient_id)
            # always, in compatible with
            # text and quick_replies

        self.data['intent'] = node_name
        return JsonResponse(self.data)

    def extract_message(self, text_response_data=None, quick_reply_response_data=None, attachment_response_data=None):
        """
        Evaluate template strings in text/quick_replies/attachments and convert them to a value.
        :param text_response_data:
        :param quick_reply_response_data:
        :param attachment_response_data:
        :rtype: Response
        """

        if self.text:
            self.data["message"]["text"] = self.text.eval(text_response_data)

        if self.quick_replies:
            self.data["message"]["quick_replies"] = self.quick_replies.eval(quick_reply_response_data)

        if self.attachments:
            if attachment_response_data:
                stringified_attachments = json.dumps(self.attachments)
                for item in attachment_response_data:
                    stringified_attachments = stringified_attachments.replace('{}', str(item), 1)
                self.attachments = json.loads(stringified_attachments)
                print('*' * 100)
            self.data["message"]["attachment"] = self.attachments

        return self

    def send(self, message, types, recipient_id):
        """
        HTTP Request to facebook endpoint to send messages
        :param message:
        :param types:
        :param recipient_id:
        :return:
        """

        data = {
            "recipient": {
                "id": recipient_id
            },
            "message": {
                type: message[type] for type in types
            }
        }

        if self.params.get('access_token'):
            # r = requests.post(
            #     "https://graph.facebook.com/v4.0/me/messages",
            #     params=self.params,
            #     headers=self.headers,
            #     data=json.dumps(data)
            # )
            # print(r.text)

            return JsonResponse(data, status=200)
        else:
            return JsonResponse({}, status=200)
