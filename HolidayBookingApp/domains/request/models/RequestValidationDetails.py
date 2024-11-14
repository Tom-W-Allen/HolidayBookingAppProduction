from common.enums.State import State
from datetime import datetime


class RequestValidationDetails:
    def __init__(self,
                 state: State,
                 message: str,
                 valid_holidays: "list[datetime]"):
        self.state = state
        self.message = message
        self.valid_holidays = valid_holidays
