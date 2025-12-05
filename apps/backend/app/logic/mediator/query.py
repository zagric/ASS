# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from logic.queries.base import BaseQuery, BaseQueryHandler


@dataclass(eq=False)
class QueryMediator[QT: BaseQuery, QR: Any](ABC):
    queries_map: dict[type(QT), BaseQueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    @abstractmethod
    def register_query(self, query: QT, query_handler: BaseQueryHandler[QT, QR]) -> QR:
        ...

    @abstractmethod
    async def handle_query(self, query: BaseQuery) -> QR:
        ...
