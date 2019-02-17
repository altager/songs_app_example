import bson
from attr import attrs, ib
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


@attrs(repr=False, slots=True)
class IntervalConverter:
    min_value = ib(default=0)
    max_value = ib(default=None)

    def __call__(self, value):

        value = int(value)

        if self.min_value is not None:
            value = self.min_value if value < self.min_value else value
        elif self.max_value is not None:
            value = self.max_value if value > self.max_value else value

        return value
