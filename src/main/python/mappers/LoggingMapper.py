from flask import session
from mappers.BaseMapper import BaseMapper
from blueprints.models.LoggingPageData import LoggingPageData
from common.Logging import get_logs
from common.enums.State import State

class LoggingMapper(BaseMapper):
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def map_initial_page_data(self):

        state = State.Normal
        message = None
        try:
            logs = get_logs()
        except Exception as ex:
            logs = []
            message = "Something went wrong and your request could not be processed. Please refresh and try again."
            state = State.Error
            session["refresh_page"] = "yes"

        return LoggingPageData(state,
                               message,
                               logs)

    def map_error(self):
        message = "Something went wrong and your request could not be processed. Please refresh and try again."
        session["refresh_page"] = "yes"
        return LoggingPageData(State.Error,
                               message,
                               [])