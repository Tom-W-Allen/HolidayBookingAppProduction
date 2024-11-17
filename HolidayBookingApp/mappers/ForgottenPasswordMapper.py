from flask import session, request
from blueprints.models.ForgottenPasswordPageData import ForgottenPasswordPageData
from common.enums.State import State
from domains.project.ProjectRepositoryInterface import IProjectRepository
from domains.request.RequestRepositoryInterface import IRequestRepository
from domains.user.UserRepositoryInterface import IUserRepository
from mappers.BaseMapper import BaseMapper


class ForgottenPasswordMapper(BaseMapper):
    def __init__(self,
                 user_repository: IUserRepository,
                 request_repository: IRequestRepository,
                 project_repository: IProjectRepository):
        self.user_repository = user_repository
        self.request_repository = request_repository
        self.project_repository = project_repository

    def map_initial_page_data(self) -> ForgottenPasswordPageData:

        return ForgottenPasswordPageData(State.Normal,
                                         None,
                                         False)

    def send_email(self) -> ForgottenPasswordPageData:

        return ForgottenPasswordPageData(State.Normal,
                                         None,
                                         True)

    def map_error(self) -> ForgottenPasswordPageData:
        message = "Something went wrong and your request could not be processed. Please refresh and try again."
        session["refresh_page"] = "yes"
        return  ForgottenPasswordPageData(State.Error,
                                          message,
                                          False)