from common.enums.State import State
from domains.user.models.PublicUser import PublicUser
from domains.request.models.Request import Request
from blueprints.models.BasePageData import BasePageData
from typing import Optional


class HomePageData(BasePageData):
    def __init__(self,
                 state: State,
                 message: Optional[str],
                 account_type: str,
                 user_details: PublicUser,
                 total_projects: int,
                 total_users: int,
                 rejected_requests: int,
                 cancelled_requests: int,
                 pending_requests: int,
                 approved_requests: int,
                 upcoming_holidays: list[Request],
                 redirect=None,
                 logout_presses=0):
        super().__init__(redirect, logout_presses)
        self.state = state
        self.message = message
        self.account_type = account_type
        self.user_details = user_details
        self.total_projects = total_projects
        self.total_users = total_users
        self.rejected_requests = rejected_requests
        self.cancelled_requests = cancelled_requests
        self.pending_requests = pending_requests
        self.approved_requests = approved_requests
        self.upcoming_holidays = upcoming_holidays

