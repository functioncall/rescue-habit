import json
import requests
from django.http import HttpResponse


def fallback_response(sender_id, page_access_token):
    """
    An error flush function, use this if errors stall the facbook chat
    :param sender_id: facebook id of a chat participant
    """
    params = {"access_token": page_access_token}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": "Sorry, service is unavailable right now. Will try to get back to you asap!"
        }
    }
    requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params=params,
        headers=headers,
        data=json.dumps(data)
    )
    return HttpResponse(status=200)
