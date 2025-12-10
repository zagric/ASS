# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from dataclasses import dataclass

from domain.exceptions.base import ApplicationError


@dataclass(eq=False)
class EntitiesCountTooLongError(ApplicationError):
    count: int

    @property
    def message(self) -> str:
        return f"Entities count too long: {self.count}"


@dataclass(eq=False)
class EntitiesCountMustBePositiveError(ApplicationError):
    count: int

    @property
    def message(self) -> str:
        return f"Entities count must be positive: {self.count}"


@dataclass(eq=False)
class BufferSizeTooLongError(ApplicationError):
    size: int

    @property
    def message(self) -> str:
        return f"Buffer size too long: {self.size}"


@dataclass(eq=False)
class BufferSizeMustBePositiveError(ApplicationError):
    size: int

    @property
    def message(self) -> str:
        return f"Buffer size must be positive: {self.size}"


@dataclass(eq=False)
class BufferSizeMustBeMoreThanZeroError(ApplicationError):
    @property
    def message(self) -> str:
        return "Buffer size must be greater than zero"


@dataclass(eq=False)
class DurationMustBeInIntervalError(ApplicationError):
    _max_duration: int

    @property
    def message(self) -> str:
        return f"Duration must be in interval between 1 and {self._max_duration}"


@dataclass(eq=False)
class RequestRateMustBeInIntervalError(ApplicationError):
    _min_request_rate: float
    _max_request_rate: float

    @property
    def message(self) -> str:
        return (
            f"Request rate must be in interval between {self._min_request_rate}"
            f" and {self._max_request_rate}"
        )
