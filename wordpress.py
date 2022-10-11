NAMESPACES = {
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "wfw": "http://wellformedweb.org/CommentAPI/",
    "wp": "http://wordpress.org/export/1.2/",
}


class Field:
    def __init__(self, key=""):
        self._key = key

    def __get__(self, obj, klass):
        if not obj:
            return self
        value = self.find(obj)
        if value is None:
            return value
        return self.transform(value)

    def __set_name__(self, klass, name):
        if not self._key:
            self._key = "_" + name
        if self._key.startswith("_"):
            self._key = ":" + klass.__name__.lower() + self._key
        if self._key.startswith(":"):
            self._key = "wp" + self._key

    def find(self, obj):
        element = obj._tree.find(self._key, NAMESPACES)
        if element.text is not None:
            value = element.text.strip()
            if value:
                return value
        return None

    def transform(self, value):
        return value


class TextField(Field):
    pass
