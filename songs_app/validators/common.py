import bson
from attr import attrs
from werkzeug.routing import BaseConverter

from songs_app.errors import SongNotFoundError


@attrs(repr=False, slots=True)
class ObjectIdConverter:
    def __call__(self, value):
        try:
            return bson.ObjectId(value)
        except bson.errors.InvalidId:
            raise ValueError


class ObjectIdURLConverter(BaseConverter):
    def to_python(self, value):
        try:
            value = ObjectIdConverter()(value)
        except ValueError:
            raise SongNotFoundError

        return value

    def to_url(self, value):
        return str(value)
