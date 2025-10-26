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
from abc import ABC
from copy import copy
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from domain.events.base import BaseEvent


@dataclass(eq=False)
class BaseEntity(ABC):  # noqa: B024
    oid: str = field(default_factory=lambda: str(uuid4()), kw_only=True)
    _events: list[BaseEvent] = field(default_factory=list, kw_only=True)
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, other: "BaseEntity") -> bool:
        return self.oid == other.oid

    def register_event(self, event: BaseEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[BaseEvent]:
        registered_events = copy(self._events)
        self._events.clear()
        
        return registered_events