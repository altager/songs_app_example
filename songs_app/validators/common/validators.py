from attr import attrs, ib


@attrs(repr=False, slots=True)
class IntervalValidator:
    min_value = ib(default=0)
    max_value = ib(default=None)

    def __call__(self, inst, attr, value):
        if not isinstance(value, int):
            raise ValueError

        if value < self.min_value:
            raise ValueError
        elif self.max_value and value > self.max_value:
            raise ValueError
