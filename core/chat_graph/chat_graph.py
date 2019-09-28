from core.chat_node.chat_node import ChatNode
from commons.errors import ChatNodeNameTypeError, ChatNodeNotFound
import os


def setup_data(obj):
    """
    1. Extracts text, quick replies, attachments from object
    2. Adds available entities to a dict and returns it
    :param obj: <dict>
    :return: <dict>
    """
    data = {}
    for prop in obj:
        if prop in ["text", "quick_replies", "attachments"]:
            data[prop] = obj[prop]
    return data


class Graph(object):
    """
    A graph which contains:
     1. chat-nodes in a layout; containing { node-name: node } as <dict>
     2. contains the start and end nodes for a chat instance.
    """
    def __init__(self, json):
        self.layout = {}
        self.json = json
        self.start = None
        self.end = None

    def get_node(self, node_name):
        """
        :param node_name: <str> should correspond to key in self.layout
        :return: <ChatNode>
        """
        if type(node_name) is not str:
            raise ChatNodeNameTypeError(node_name)
        if node_name not in self.layout:
            raise ChatNodeNotFound(node_name)
        return self.layout[node_name]["node"]

    def node_in_graph(self, node_name):
        if type(node_name) is not str:
            raise ChatNodeNameTypeError(node_name)
        elif node_name in self.layout:
            return True
        else:
            raise ChatNodeNotFound(node_name)

    def get_node_triggers(self, node_name):
        """
        Use if regular expression based triggers are provided
        :param node_name:
        :return:
        """
        return self.layout[node_name]["triggers"]

    def draw_graph(self):
        """
        sets up graph instance after reading json file
        """
        for i, prop in enumerate(self.json):
            nxt = prop["next"] if "next" in self.json[i] else None
            pre = prop["pre"] if "pre" in self.json[i] else None
            cn = ChatNode(prop["name"], setup_data(self.json[i]), nxt, pre)
            self.layout[prop["name"]] = {
                "node": cn,
                "triggers": self.json[i]["triggers"] if "triggers" in self.json[i] else []
            }
            if self.start is None:
                self.start = cn
            self.end = cn
