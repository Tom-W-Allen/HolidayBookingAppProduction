from common.enums.State import State
from typing import Optional


class LoginPageData:
    def __init__(self, redirect: Optional[str], state: State, message: Optional[str], signing_up: bool):
        self.redirect = redirect
        self.state = state
        self.message = message
        self.signing_up = signing_up
