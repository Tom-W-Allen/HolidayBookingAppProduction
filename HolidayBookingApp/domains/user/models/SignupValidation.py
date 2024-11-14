from common.enums.State import State
from typing import Optional


class SignupValidation:
    def __init__(self, state: State, message: Optional[str]):
        self.state = state
        self.message = message
