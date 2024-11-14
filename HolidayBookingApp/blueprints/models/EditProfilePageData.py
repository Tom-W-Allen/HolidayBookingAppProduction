from common.enums.State import State
from common.enums.UserType import UserType
from domains.user.models.PublicUser import PublicUser
from blueprints.models.BasePageData import BasePageData
from typing import Optional


class EditProfilePageData(BasePageData):
    def __init__(self,
                 state: State,
                 message: Optional[str],
                 account_type: UserType,
                 selected_user: int,
                 employee_list: "list[PublicUser]",
                 user_details: PublicUser,
                 manager_list: "list[PublicUser]",
                 approval_required: bool,
                 delete_button_presses: int,
                 base_id: int,
                 selected_manager: int,
                 redirect=None,
                 logout_presses=0):
        super().__init__(redirect, logout_presses)
        self.state = state
        self.message = message
        self.account_type = account_type
        self.selected_user = selected_user
        self.employee_list = employee_list
        self.user_details = user_details
        self.manager_list = manager_list
        self.approval_required = approval_required
        self.delete_button_presses = delete_button_presses
        self.base_id = base_id
        self.selected_manager = selected_manager
