from typing import Optional

from attr import attrs, ib

from songs_app.validators.common import ObjectIdConverter, IntervalValidator


@attrs(slots=True, frozen=True)
class CreateRating:
    song_id: Optional[str] = ib(default=None, converter=ObjectIdConverter())
    rating: Optional[str] = ib(default=None, validator=IntervalValidator(min_value=1, max_value=5))
