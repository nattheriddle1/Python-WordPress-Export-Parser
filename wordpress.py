from datetime import datetime
from xml.etree import ElementTree

DATETIME_FORMATS = {
    "rss": r"%a, %d %b %Y %H:%M:%S %z",
    "wp": r"%Y-%m-%d %H:%M:%S",
}

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


class IntegerField(Field):
    def transform(self, value):
        return int(value)


class BooleanField(Field):
    def __init__(self, key="", true={}, false={}):
        super().__init__(key)
        self._true = true
        self._false = false

    def transform(self, value):
        if value in self._true:
            return True
        elif value in self._false:
            return False


class DateTimeField(Field):
    def __init__(self, key="", format=DATETIME_FORMATS["wp"]):
        super().__init__(key)
        self._format = format

    def transform(self, value):
        return datetime.strptime(value, self._format)


class Model:
    def __init__(self, tree):
        self._tree = tree


class Meta(Model):
    key = TextField()
    value = TextField()


class Author(Model):
    id = IntegerField()
    username = TextField(key="_login")
    email = TextField()
    name = TextField(key="_display_name")
    first_name = TextField()
    last_name = TextField()


class Category(Model):
    id = IntegerField(key=":term_id")
    name = TextField(key=":cat_name")
    slug = TextField(key="_nicename")
    description = TextField()
