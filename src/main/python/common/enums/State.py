from enum import Enum


class State(Enum):
    Error = -2
    Warning = -1,
    Normal = 0,
    Information = 1,
    Success = 2,
