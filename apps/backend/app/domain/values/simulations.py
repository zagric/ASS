# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# 
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
# 
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from dataclasses import dataclass

from domain.exceptions.simulations import (
    BufferSizeMustBePositiveError,
    BufferSizeTooLongError,
    EntitiesCountMustBePositiveError,
    EntitiesCountTooLongError,
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
        if self.value < 0:
            raise BufferSizeMustBePositiveError(self.value)

        if self.value > self._max_length:
            raise BufferSizeTooLongError(self.value)

    def as_generic_type(self) -> int:
        return int(self.value)