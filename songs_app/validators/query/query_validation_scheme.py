from typing import Optional

import bson
from attr import attrs, attrib, ib
from attr.converters import optional as opt_conv


@attrs(repr=False, slots=True)
class IntervalConverter:
    min_value = attrib(default=0)
    max_value = attrib(default=None)

    def __call__(self, value):

        value = int(value)

        if self.min_value is not None:
            value = self.min_value if value < self.min_value else value
        elif self.max_value is not None:
            value = self.max_value if value > self.max_value else value

        return value


@attrs(repr=False, slots=True)
class ObjectIdConverter:
    def __call__(self, value):
        try:
            return bson.ObjectId(value)
        except bson.errors.InvalidId:
            raise ValueError


@attrs(slots=True, frozen=True)
class GetLimitLastId:
    limit: Optional[int] = ib(default=5, converter=IntervalConverter(min_value=1, max_value=100))
    last_id: Optional[str] = ib(default=None, converter=opt_conv(ObjectIdConverter()))


@attrs(slots=True, frozen=True)
class GetLevel:
    level: Optional[int] = ib(default=None, converter=int)
