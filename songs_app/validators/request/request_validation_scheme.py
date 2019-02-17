from typing import Optional

from attr import attrs, attrib, ib

from songs_app.validators.common import ObjectIdConverter


@attrs(repr=False, slots=True)
class IntervalValidator:
    min_value = attrib(default=0)
    max_value = attrib(default=None)

    def __call__(self, inst, attr, value):
        if value < self.min_value:
            raise ValueError
        elif self.max_value and value > self.max_value:
            raise ValueError


@attrs(slots=True, frozen=True)
class CreateRating:
    song_id: Optional[str] = ib(default=None, converter=ObjectIdConverter())
    rating: Optional[str] = ib(default=None, validator=IntervalValidator(min_value=1, max_value=5))
