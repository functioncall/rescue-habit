from core.node.node import Node
from messenger.utils.response.response import Response


class ChatNode(Node):
    """
    ChatNode, inherits Node Class,
    represents a node in a chat-flow
    """
    def __init__(self, name, data=None, nxt=None, pre=None):
        """
        :param name: <str>
        :param data: <object>
        :param nxt: <list>
        :param pre: <list>
        """
        if pre is None:
            pre = []
        if nxt is None:
            nxt = []
        if data is not None:
            data = Response(data)
        super(ChatNode, self).__init__(name, data, nxt, pre)
