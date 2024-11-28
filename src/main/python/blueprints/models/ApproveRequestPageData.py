from common.enums.State import State
from domains.user.models.PublicUser import PublicUser
from domains.request.models.Request import Request
from blueprints.models.BasePageData import BasePageData
from typing import Optional


class ApproveRequestPageData(BasePageData):
    def __init__(self,
                 state: State,
                 message: Optional[str],
                 employee_list: "list[PublicUser]",
                 selected_user: int,
                 request_list: "list[Request]",
                 approval_required: Optional[int],
                 approval_state: Optional[str],
                 account_type: str,
                 redirect=None,
                 logout_presses=0):
        super().__init__(redirect, logout_presses)
        self.state = state
        self.message = message
        self.employee_list = employee_list
        self.selected_user = selected_user
        self.request_list = request_list
        self.approval_required = approval_required
        self.approval_state = approval_state
        self.account_type = account_type
