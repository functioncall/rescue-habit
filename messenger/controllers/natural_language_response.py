import traceback
from constants import KEYS, CAPS
from data_functions.data_functions import function_data_map
# from interpreter_unit.interpreter_unit import Interpreter
from django.conf import settings


def user_defined_type_response(chat_graph, text, sender_id, page_access_token, page_id):
    """
    Handles User defined inputs: natural language
    :param formatted_message: the message received as natural language input
    :param sender_id: facebook id of a chat participant
    """
    try:
        # nlp_api = Interpreter()

        # if page_access_token == 'awiros':
        #     node_name = nlp_api.faq_query(text)
        # else:
        #     node_name = nlp_api.facebook_query(text)
        node_name = ""

        print("node name: ", node_name)

        return chat_graph.get_node(node_name).data.extract_message(
            text_response_data=function_data_map(node_name)[KEYS.TXT](**{
                KEYS.FB_ID: sender_id,
                KEYS.PAGE_ACCESS_TOKEN: page_access_token,
                KEYS.PAGE_ID: page_id
            }),
            quick_reply_response_data=function_data_map(node_name)[KEYS.QR](),
            attachment_response_data=function_data_map(node_name)[KEYS.AT](**{
                KEYS.FB_ID: sender_id,
                KEYS.PAGE_ACCESS_TOKEN: page_access_token,
                KEYS.PAGE_ID: page_id
            })
        ).send_to(sender_id, page_access_token, node_name)
    except Exception as e:
        settings.LOGGER.info('message', extra={
            'event': 'handle_messenger:: {}'.format(e),
            'payload': traceback.format_exc()
        })
        raise e.__class__(e)
