from enum import Enum


class RequestStatus(Enum):
    pending = 0,
    approved = 1,
    rejected = 2,
    cancelled = 3,

