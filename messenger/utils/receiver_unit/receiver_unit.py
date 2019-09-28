from constants import KEYS, STRINGS, CAPS
from commons.logger import log


class MessengerMessageParser(object):
    def __init__(self):
        self.action = None
        self.content = None
        self.type = CAPS.FIXED

    def set(self, action=None, content=None, type=CAPS.FIXED):
        self.action = action
        self.content = content
        self.type = type

    def _has_postback(self, messaging_event):
        content = None
        message_payload = messaging_event \
            .get(KEYS.POSTBACK, {}) \
            .get(KEYS.PAYLOAD)
        if not message_payload:
            return None

        if STRINGS.POSTBACK_PAYLOAD_SEPARATOR in message_payload:
            action, content = message_payload.split(STRINGS.POSTBACK_PAYLOAD_SEPARATOR, 1)
        else:
            action = message_payload
        self.set(action=action, content=content, type=CAPS.FIXED)

    def _has_natural_language(self, messaging_event):
        content = messaging_event \
            .get(KEYS.MESSAGE, {}) \
            .get(KEYS.TEXT)
        if not content:
            return None
        self.set(content=content, type=CAPS.USER_DEFINED)

    def _has_quick_reply(self, messaging_event):
        message_payload = messaging_event \
            .get(KEYS.MESSAGE, {}) \
            .get(KEYS.QUICK_REPLY, {}) \
            .get(KEYS.PAYLOAD)
        if not message_payload:
            return None
        if STRINGS.POSTBACK_PAYLOAD_SEPARATOR in message_payload:
            action, content = message_payload.split(STRINGS.POSTBACK_PAYLOAD_SEPARATOR, 1)
        else:
            action, content = message_payload, message_payload

        self.set(type=CAPS.FIXED, content=content, action=action)

    @staticmethod
    def get_sender_id(messaging_event):
        return messaging_event.get(KEYS.SENDER, {}).get(KEYS.ID)

    def get_parsed_message(self, message):
        """
        :rtype: tuple
        :param message: <dict>
        :return: <tuple>(size=2): formatted message object as user defined or fixed along with sender id.
        """
        if not message.get(KEYS.OBJECT) == STRINGS.PAGE:
            return None

        messaging_entry = message.get(KEYS.ENTRY, [])

        if len(messaging_entry) == 0:
            return None

        messaging_events = messaging_entry[0].get(KEYS.MESSAGING)
        messaging_event = messaging_events[0] if len(messaging_events) > 0 else None
        sender_id = MessengerMessageParser.get_sender_id(messaging_event)
        if messaging_event is None:
            return None, sender_id
        return self._message_handler(messaging_event), sender_id

    def _message_handler(self, messaging_event):
        self._has_postback(messaging_event)
        self._has_quick_reply(messaging_event)
        self._has_natural_language(messaging_event)
        return {
            KEYS.ACTION: self.action,
            KEYS.CONTENT: self.content,
            KEYS.TYPE: self.type
        }


messenger_message_parser = MessengerMessageParser()
