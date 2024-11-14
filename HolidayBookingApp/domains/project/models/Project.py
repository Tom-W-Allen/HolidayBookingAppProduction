from datetime import datetime


class Project:
    def __init__(self,
                 project_id: int,
                 project_name: str,
                 start_date: datetime,
                 end_date: datetime,
                 project_lead: int):
        self.project_id = project_id
        self.project_name = project_name
        self.start_date = start_date
        self.end_date = end_date
        self.project_lead = project_lead
