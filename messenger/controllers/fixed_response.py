from data_functions.data_functions import function_data_map
from constants import KEYS


def fixed_type_response(chat_graph, message, sender_id, page_access_token):
    """
    Handles Fixed type inputs: postback/quick_reply
    :param page_access_token:
    :param chat_graph:
    :param message: the message received as payload of the postback/quick_reply
    :param sender_id: facebook id of a chat participant
    """

    node_name = message.get(KEYS.ACTION)

    return chat_graph.get_node(node_name)\
        .data \
        .extract_message(
            text_response_data=function_data_map(node_name)[KEYS.TXT](**{
                KEYS.SENDER_ID: sender_id,
                KEYS.MESSAGE: message
            }),
            quick_reply_response_data=function_data_map(node_name)[KEYS.QR](),
            attachment_response_data=function_data_map(node_name)[KEYS.AT]()
        ) \
        .send_to(sender_id, page_access_token, node_name)
