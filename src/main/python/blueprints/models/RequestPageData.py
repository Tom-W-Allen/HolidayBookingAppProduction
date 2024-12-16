from domains.request.models.RequestDates import RequestDates
from domains.request.models.Request import Request
from domains.user.models.PublicUser import PublicUser
from blueprints.models.BasePageData import BasePageData
from typing import Optional


class BaseRequestPageData(BasePageData):
    def __init__(self,
                 remaining_holidays: int,
                 pending_holidays: int,
                 basic_users: "list[PublicUser]",
                 request_list: "list[Request]",
                 manager: Optional[int],
                 base_user: int,
                 redirect=None,
                 logout_presses=0):
        super().__init__(redirect, logout_presses)
        self.remaining_holidays = remaining_holidays
        self.pending_holidays = pending_holidays
        self.basic_users = basic_users
        self.request_list = request_list
        self.manager = manager
        self.base_user = base_user


class FullRequestPageData(BaseRequestPageData):
    def __init__(self,
                 state: str,
                 message: Optional[str],
                 remaining_holidays: int,
                 pending_holidays: int,
                 account_type: str,
                 user_id: int,
                 selected_dates: Optional[RequestDates],
                 basic_users: "list[PublicUser]",
                 request_list: "list[Request]",
                 approval_required: Optional[int],
                 manager: Optional[int],
                 base_user: int,
                 redirect=None,
                 logout_presses=0):
        super().__init__(remaining_holidays, pending_holidays, basic_users,
                         request_list, manager, base_user, redirect, logout_presses)
        self.state = state
        self.message = message
        self.account_type = account_type
        self.user_id = user_id
        self.selected_dates = selected_dates
        self.approval_required = approval_required
