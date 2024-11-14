from common.enums.State import State
from domains.user.models.PublicUser import PublicUser
from blueprints.models.BasePageData import BasePageData
from typing import Optional


class CreateProjectPageData(BasePageData):
    def __init__(self,
                 state: State,
                 message: Optional[str],
                 manager_list: "list[PublicUser]",
                 redirect=None,
                 logout_presses=0):
        super().__init__(redirect, logout_presses)
        self.state = state
        self.message = message
        self.manager_list = manager_list
