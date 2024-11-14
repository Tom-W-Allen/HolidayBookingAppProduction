from flask import request, session
from common.enums.State import State
from common.enums.UserType import UserType
from blueprints.models.CreateProjectPageData import CreateProjectPageData
from domains.project.ProjectRepositoryInterface import IProjectRepository
from domains.user.UserRepositoryInterface import IUserRepository
from mappers.BaseMapper import BaseMapper


class CreateProjectPageMapper(BaseMapper):
    def __init__(self, user_repository: IUserRepository, project_repository: IProjectRepository):
        self.user_repository = user_repository
        self.project_repository = project_repository

    def map_initial_page_data(self) -> CreateProjectPageData:

        manager_list = self.user_repository.get_user_type_details(UserType.manager)

        if session["account_type"] == "manager":
            manager_list = [x for x in manager_list if x.user_id == int(session["_user_id"])]

        return CreateProjectPageData(State.Normal,
                                     None,
                                     manager_list)

    def map_create_project(self) -> CreateProjectPageData:

        manager_list = self.user_repository.get_user_type_details(UserType.manager)

        if session["account_type"] == "manager":
            manager_list = [x for x in manager_list if x.user_id == int(session["_user_id"])]

        validation_details = self.project_repository.validate_project_dates(request.form["Start Date"],
                                                                            request.form["End Date"],
                                                                            request.form["Name"])

        message = validation_details.message

        if validation_details.state == State.Success:
            self.project_repository.create_project(request.form["Name"],
                                                   request.form["Start Date"],
                                                   request.form["End Date"],
                                                   int(request.form["Manager"]))

            message = "Project created successfully"

        return CreateProjectPageData(validation_details.state,
                                     message,
                                     manager_list)

    def map_error(self) -> CreateProjectPageData:

        try:
            manager_list = self.user_repository.get_user_type_details(UserType.manager)

            if session["account_type"] == "manager":
                manager_list = [x for x in manager_list if x.user_id == int(session["_user_id"])]
        except:
            manager_list = []

        message = "Something went wrong and your request could not be processed. Please refresh and try again."

        return CreateProjectPageData(State.Error,
                                     message,
                                     manager_list)
