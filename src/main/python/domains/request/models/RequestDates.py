from datetime import datetime


class RequestDates:
    def __init__(self,
                 start_date: str,
                 end_date: str,
                 valid_start_date: datetime,
                 valid_end_date: datetime,
                 holidays: "list[datetime]"):
        self.start_date = start_date
        self.end_date = end_date
        self.valid_start_date = valid_start_date
        self.valid_end_date = valid_end_date
        self.holidays = holidays
