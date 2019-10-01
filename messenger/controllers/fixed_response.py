from data_functions.data_functions import function_data_map
from constants import KEYS
from survey import survey


def fixed_type_response(chat_graph, message, sender_id, page_access_token):
    """
    Handles Fixed type inputs: postback/quick_reply
    :param page_access_token:
    :param chat_graph:
    :param message: the message received as payload of the postback/quick_reply
    :param sender_id: facebook id of a chat participant
    """

    node_name = message.get(KEYS.ACTION)
    survey_obj = survey.Survey(user_fb_id=sender_id)
    content = message.get(KEYS.CONTENT).split('_')
    print(len(content))
    if not survey_obj.is_active():
        survey_obj.create_survey()
        survey_instance = survey_obj.get_current_instance()
    elif len(content) <= 1:
        survey_instance = survey_obj.get_current_instance()
    else:
        post_id = content[0]
        survey_response = content[1]

        survey_obj.store_survey_response(post_id=post_id, post_response=survey_response)
        survey_instance = survey_obj.get_current_instance()

        if survey_instance is None:
            survey_obj.clear_survey_state()
            node_name = "POST_SURVEY"

    return chat_graph.get_node(node_name) \
        .data \
        .extract_message(
            text_response_data=function_data_map(node_name)[KEYS.TXT](**{
                KEYS.SENDER_ID: sender_id,
                KEYS.SURVEY_INSTANCE: survey_instance
            }),
            quick_reply_response_data=function_data_map(node_name)[KEYS.QR](**{
                KEYS.SENDER_ID: sender_id,
                KEYS.SURVEY_INSTANCE: survey_instance
            }),
            attachment_response_data=function_data_map(node_name)[KEYS.AT]()
        ) \
        .send_to(sender_id, page_access_token, node_name)
