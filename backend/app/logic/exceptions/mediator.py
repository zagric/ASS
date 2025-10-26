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

from logic.exceptions.base import LogicError


@dataclass(eq=False)
class EventHandlersNotRegisteredError(LogicError):
    event_type: type

    @property
    def message(self):
        return f"Event handlers could not be found for: {self.event_type}"


@dataclass(eq=False)
class CommandHandlersNotRegisteredError(LogicError):
    command_type: type

    @property
    def message(self):
        return f"Command handlers could not be found for: {self.command_type}"