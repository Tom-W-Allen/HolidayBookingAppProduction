from mappers.BaseMapper import BaseMapper
from blueprints.models.LoggingPageData import LoggingPageData
from common.Logging import get_logs

class LoggingMapper(BaseMapper):
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def map_initial_page_data(self):
        logs = get_logs()
        return LoggingPageData(logs)
