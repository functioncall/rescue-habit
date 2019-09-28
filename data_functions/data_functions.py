import ast
import json
import os
import random
import traceback

import requests
from django.conf import settings
from django.core import serializers
from django.core.cache import cache

from commons.emoji import EMOJI
from commons.errors import ChatNodeNotFound, ChatNodeNameTypeError
from constants import KEYS, CAPS


def add_emoji(**args):
    return [{
        "thinking_emoji": ''.join(EMOJI["thinking"])
    }]


def no_op(**args):
    return {}


# def do_small_talk(**args):
#     user_profile = get_profile(args[KEYS.FB_ID], args[KEYS.PAGE_ACCESS_TOKEN])
#     print("user_profile: ", user_profile)
#     restaurant_info = requests.post(os.environ.get('API_URL') + '/restaurant/get_details', json={
#         "page_id": args['page_id']
#     })
#     return [{
#         "first_name": user_profile.username,
#         "happy_emoji": random.choice(EMOJI["happy"]),
#     }]


def get_button_payload(item):
    items_as_dict = json.loads(serializers.serialize('json', [item]))
    item_as_dict = items_as_dict[0].get('fields')
    item_as_dict.update({'item_id': item.id })

    return "CART_UPDATE_ITEM/{}".format(item_as_dict)



def attach_emoji(**args):
    return [{
        "emoji": EMOJI["thinking"][0]
    }]


def add_value_count(**args):
    cache_key = '{}_{}'.format(args.get(KEYS.FB_ID), CAPS.CART_UPDATE_ITEM)

    items = [ast.literal_eval(item) for item in ast.literal_eval(cache.get(cache_key))]

    return [{
        "item": items[-1].get('item_name'),
        "item_count": str(len(items)),
        "item_price": '{0:.2f}'.format(sum([float(item.get('item_price')) for item in items])),
        "reaction": ''.join([random.choice(EMOJI["happy"]), random.choice(EMOJI["success"]), random.choice(EMOJI["heart"])])
    }]


# def interact_with_username(**args):
#     print("IAMHERENOW")
#
#     user_profile = get_profile(args['fb_id'], args['page_access_token'])
#     print("user_profile: ", user_profile)
#
#     return [{
#         "first_name": user_profile.username,
#         "reaction": ''.join([random.choice(EMOJI["happy"]), random.choice(EMOJI["heart"])])
#     }]


def add_sadness(**args):
    return [{
        'reactions': ''.join(EMOJI["sad"]),
        'order_id': args['order_id']
    }]


def add_joy(**args):
    return [{
        'reactions': '{}{}'.format(''.join(EMOJI["success"]), ''.join(EMOJI['heart'])),
        'order_id': args['order_id']
    }]


def add_happy(**args):
    return [{
        'reactions': '{}{}'.format(''.join(EMOJI["success"]), ''.join(EMOJI['happy'])),
        'order_id': args['order_id']
    }]


def attach_survey_text(**args):

    return [{
        "habit": "coding"
    }]


node_function_map = {
    'SMALL_TALK': {
        "txt": no_op,
        "qr": no_op,
        "at": no_op
    },
    'SURVEY': {
        "txt": attach_survey_text,
        "qr": no_op,
        "at": no_op
    },
    'GETTING_STARTED': {
        "txt": no_op,
        "qr": no_op,
        "at": no_op
    },
    "NO_OP": {
        "txt": no_op,
        "qr": no_op,
        "at": no_op
    }
}


def function_data_map(node_name):
    """
    Returns a chat-node if found in chat-graph layout.
    :param node_name: <str>
    :return: <ChatNode>
    """
    pass

    if node_name not in node_function_map:
        return {
            "txt": no_op,
            "qr": no_op,
            "at": no_op
        }
    return node_function_map[node_name]
