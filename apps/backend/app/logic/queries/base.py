# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BaseQuery(ABC):  # noqa: B024
    ...


@dataclass(frozen=True)
class BaseQueryHandler[QT: BaseQuery, QR: Any](ABC):
    @abstractmethod
    async def handle(self, query: QT) -> QR:
        ...
