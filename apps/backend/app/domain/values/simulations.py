# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from dataclasses import dataclass

from domain.exceptions.simulations import (
    BufferSizeMustBeMoreThanZeroError,
    BufferSizeMustBePositiveError,
    BufferSizeTooLongError,
    DurationMustBeInIntervalError,
    EntitiesCountMustBePositiveError,
    EntitiesCountTooLongError,
    RequestRateMustBeInIntervalError,
)
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class EntitiesCount(BaseValueObject[int]):
    _max_length: int = 1_000

    def validate(self) -> None:
        if self.value < 0:
            raise EntitiesCountMustBePositiveError(self.value)

        if self.value > self._max_length:
            raise EntitiesCountTooLongError(self.value)

    def as_generic_type(self) -> int:
        return int(self.value)


@dataclass(frozen=True)
class BufferSize(BaseValueObject[int]):
    _max_length: int = 10_000

    def validate(self) -> None:
        if self.value == 0:
            raise BufferSizeMustBeMoreThanZeroError

        if self.value < 0:
            raise BufferSizeMustBePositiveError(self.value)

        if self.value > self._max_length:
            raise BufferSizeTooLongError(self.value)

    def as_generic_type(self) -> int:
        return int(self.value)


@dataclass(frozen=True)
class Duration(BaseValueObject[int]):
    _max_length: int = 3_600

    def validate(self) -> None:
        if self.value <= 0 or self.value > self._max_length:
            raise DurationMustBeInIntervalError(self._max_length)

    def as_generic_type(self) -> int:
        return int(self.value)


@dataclass(frozen=True)
class RequestRate(BaseValueObject[float]):
    _min_length: float = 0.5
    _max_length: float = 5

    def validate(self) -> None:
        if self.value < self._min_length or self.value > self._max_length:
            raise RequestRateMustBeInIntervalError(self._min_length, self._max_length)

    def as_generic_type(self) -> float:
        return float(self.value)
