from datetime import datetime
from decimal import Decimal

from attr import attrs, ib
from bson import ObjectId


@attrs(slots=True, frozen=True)
class SongResponse:
    id: str = ib()
    artist: str = ib()
    title: str = ib()
    difficulty: Decimal = ib()
    level: Decimal = ib()
    released: str = ib()

    @id.validator
    def id_validator(self, attribute, value):
        ObjectId(value)

    @released.validator
    def released_validator(self, attribute, value):
        datetime.strptime(value, "%Y-%m-%d")


@attrs(slots=True)
class AvgDifficultyResponse:
    average_difficulty: Decimal = ib()
    level: int = ib()
