from blueprints.models.BasePageData import BasePageData


class LoggingPageData(BasePageData):
    def __init__(self, state, message, logs, redirect=None, logout_presses=0):
        super().__init__(redirect, logout_presses)
        self.state = state
        self.message = message
        self.logs = logs