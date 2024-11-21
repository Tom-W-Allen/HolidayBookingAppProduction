from common.enums.State import State
from blueprints.models.BasePageData import BasePageData
from typing import Optional


class ForgottenPasswordPageData(BasePageData):
    def __init__(self,
                 state: State,
                 message: Optional[str],
                 successful_reset: bool,
                 redirect=None,
                 logout_presses=0):
        super().__init__(redirect, logout_presses)
        self.state = state
        self.message = message
        self.successful_reset = successful_reset