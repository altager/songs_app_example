from typing import Optional

from attr import attrs, ib
from attr.converters import optional as opt_conv
from attr.validators import optional as opt_val

from songs_app.validators.common import (
    ObjectIdConverter,
    IntervalConverter,
    IntervalValidator,
)


@attrs(slots=True, frozen=True)
class GetLimitLastId:
    limit: Optional[int] = ib(
        default=5, converter=IntervalConverter(min_value=1, max_value=100)
    )
    last_id: Optional[str] = ib(default=None, converter=opt_conv(ObjectIdConverter()))


@attrs(slots=True, frozen=True)
class GetLevel:
    level: Optional[int] = ib(
        default=None,
        converter=opt_conv(int),
        validator=opt_val(IntervalValidator(min_value=0)),
    )


@attrs(slots=True, frozen=True)
class Search:
    message: str = ib(default="")
