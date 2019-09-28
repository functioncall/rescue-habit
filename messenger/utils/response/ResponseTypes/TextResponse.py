from messenger.utils.response.ResponseTypes.Template import Template


class TextResponse(object):
    """
    TextResponse templatizes text
    """

    def __init__(self, text):
        self.text = [Template(t) for t in text]

    def eval(self, collection=None):
        """
        Evaluate the value of template using the map in collection
        :param collection: <list>
        :return: <list::str>
        """
        if not collection:
            return self.text[0].template
        l_coll = len(collection) if isinstance(collection, list) else 0       # if collection is NoneType.
                                                                    # take length as 0, NoneType has no len().

        return [t.out(collection[i])                                # evaluate template-string with value in collection.
                  if i < l_coll                                     # else output template string as is.
                  else t.template for i, t in enumerate(self.text)][0]
