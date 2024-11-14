from datetime import datetime


class Request:
    def __init__(self,
                 record_id: int,
                 first_name: str,
                 surname: str,
                 start_date: datetime,
                 end_date: datetime,
                 total_holidays: int,
                 status: str):
        self.id = record_id
        self.first_name = first_name
        self.surname = surname
        self.start_date = start_date
        self.end_date = end_date
        self.total_holidays = total_holidays
        self.status = status
