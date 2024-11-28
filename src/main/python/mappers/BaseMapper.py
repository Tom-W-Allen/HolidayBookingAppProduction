from flask import request
from flask_login import logout_user
from typing import Optional


class BaseMapper:

    def map_logout(self):

        if int(request.form["logout presses"]) == 1:
            return self.create_logout_object(1, None)
        else:
            page_data = self.create_logout_object(0, "/login")
            logout_user()
            return page_data

    def create_logout_object(self, logout_button_presses: int, redirect: Optional[str]):
        base_data = self.map_initial_page_data()
        base_data.logout_presses = logout_button_presses
        base_data.redirect = redirect

        return base_data

    def map_initial_page_data(self) -> any:
        pass
