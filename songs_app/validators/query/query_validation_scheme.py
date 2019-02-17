from typing import Optional

from attr import attrs, attrib, ib
from attr.converters import optional as opt_conv

from songs_app.validators.common import ObjectIdConverter


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


@attrs(slots=True, frozen=True)
class GetLimitLastId:
    limit: Optional[int] = ib(default=5, converter=IntervalConverter(min_value=1, max_value=100))
    last_id: Optional[str] = ib(default=None, converter=opt_conv(ObjectIdConverter()))


@attrs(slots=True, frozen=True)
class GetLevel:
    level: Optional[int] = ib(default=None, converter=opt_conv(int))


@attrs(slots=True, frozen=True)
class Search:
    message: str = ib(default="")
