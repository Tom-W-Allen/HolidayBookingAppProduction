from typing import Optional


class BasePageData:
    def __init__(self, redirect: Optional[str], logout_presses=0):
        self.logout_presses = logout_presses
        self.redirect = redirect
