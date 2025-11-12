# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025. All rights reserved.
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