from common.enums.UserType import UserType
from datetime import datetime


class ProjectMember:
    def __init__(self,
                 user_id: int,
                 user_name: str,
                 account_type: UserType,
                 first_name: str,
                 surname: str,
                 project_holidays: "list[datetime]"):
        self.user_id = user_id
        self.user_name = user_name
        self.account_type = account_type
        self.first_name = first_name
        self.surname = surname
        self.project_holidays = project_holidays
