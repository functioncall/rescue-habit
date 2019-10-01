import ast
import json
import os
import traceback

import requests
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from enum import Enum

from django_project import settings
from constants import HEADERS, KEYS, CAPS
from core.chat_graph.chat_graph import Graph
from data_functions.data_functions import function_data_map
from messenger.controllers.fallback_response import fallback_response
from messenger.controllers.fixed_response import fixed_type_response
from messenger.utils.receiver_unit.receiver_unit import messenger_message_parser


def retrieve_chat_graph(page_access_token=None, page_id=None):
    json_chat_flow_path = os.path.join(os.getcwd(), "core/chat_graph/graph_config.json")
    with open(json_chat_flow_path, "r") as json_chat_flow_file:
        json_chat_flow = json.load(json_chat_flow_file)

    chat_graph = Graph(json_chat_flow)
    chat_graph.draw_graph()
    return chat_graph


def init_chat_flow(request):
    message = json.loads(request.body.decode("utf-8"))

    # settings.LOGGER.info('message', extra={
    #     'event': 'USER_MESSAGE',
    #     'payload': message
    # })

    page_access_token = "EAAaJsZB2kUBgBAK60QkIQnO0cqzFGmjBlcxUdFZB6ZCLfeNOF2Me2qGiWDfURloSTQJHiQEPpELYHImW3Loi6jIejOchElLjuY5ZCns0JYghdvAjMMtbZARKNsO0cCB4laifbtwfF78vxoYzJ5EDERXCYXkGvTzINAOnr6jTGBViW8CPO1ECR"
    page_id = "533241540430171" # request.META[HEADERS.HTTP_PAGE_ID]
    message, sender_id = messenger_message_parser.get_parsed_message(message)
    chat_graph = retrieve_chat_graph(page_access_token, page_id)

    return sender_id, page_id, page_access_token, message, chat_graph


def handle_messenger_message(request):
    """
    route a message to user defined or fixed type
    :param request: message received by web-server

    """

    try:
        sender_id, page_id, page_access_token, message, chat_graph = init_chat_flow(request)
    except Exception as e:
        # settings.LOGGER.info('message', extra={
        #     'event': 'handle_messenger:: {}'.format(e),
        #     'payload': traceback.format_exc()
        # })
        return HttpResponse(status=200)

    try:
        # settings.LOGGER.info('message', extra={
        #     'event': 'PARSED_MESSAGE',
        #     'payload': message
        # })

        if message.get(KEYS.TYPE) == CAPS.FIXED:
            return fixed_type_response(chat_graph, message, sender_id, page_access_token)
        # else:
        #     return user_defined_type_response(chat_graph, message[KEYS.CONTENT], sender_id, page_access_token)
    except Exception as e:
        # settings.LOGGER.info('message', extra={
        #     'event': 'handle_messenger:: {}'.format(e),
        #     'payload': traceback.format_exc()
        # })
        print(e)
        return fallback_response(sender_id, page_access_token)
