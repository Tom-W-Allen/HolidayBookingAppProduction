from blueprints.models.BasePageData import BasePageData


class LoggingPageData(BasePageData):
    def __init__(self, logs, redirect=None, logout_presses=0):
        super().__init__(redirect, logout_presses)
        self.logs = logs