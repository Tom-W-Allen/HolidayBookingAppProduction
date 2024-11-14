from blueprints.models.HomePageData import HomePageData
from domains.user.UserRepositoryInterface import IUserRepository
from domains.request.RequestRepositoryInterface import IRequestRepository
from domains.project.ProjectRepositoryInterface import IProjectRepository
from common.enums.RequestStatus import RequestStatus
from common.enums.State import State
from flask import session
from datetime import datetime
from domains.user.models.PublicUser import PublicUser
from mappers.BaseMapper import BaseMapper


class HomePageMapper(BaseMapper):
    def __init__(self,
                 user_repository: IUserRepository,
                 request_repository: IRequestRepository,
                 project_repository: IProjectRepository):
        self.user_repository = user_repository
        self.request_repository = request_repository
        self.project_repository = project_repository

    def map_initial_page_data(self):

        user_details = self.user_repository.get_public_user_details(int(session["_user_id"]))
        total_users = []
        rejected_requests = []
        cancelled_requests = []
        approved_requests = []
        upcoming_holidays = []

        if session["account_type"] == 'admin':
            total_projects = self.project_repository.get_all_projects()
            total_users = self.user_repository.get_all_users()
            rejected_requests = self.request_repository.get_all_requests_by_status(RequestStatus.rejected)
            cancelled_requests = self.request_repository.get_all_requests_by_status(RequestStatus.cancelled)
            pending_requests = self.request_repository.get_all_requests_by_status(RequestStatus.pending)
            approved_requests = self.request_repository.get_all_requests_by_status(RequestStatus.approved)
        elif session["account_type"] == 'manager':
            total_projects = self.project_repository.get_manager_projects(int(session["_user_id"]))
            pending_requests = self.request_repository.get_requests_for_approval(int(session["_user_id"]))
        else:
            request_history = self.request_repository.get_requests_for_review(int(session["_user_id"]))
            current_date = datetime.now()

            total_projects = self.project_repository.get_employee_projects(int(session["_user_id"]))
            pending_requests = [x for x in request_history if x.status == 'pending']
            upcoming_holidays = [x for x in request_history if x.status == 'approved' and x.start_date > current_date]

        return HomePageData(State.Normal,
                            None,
                            session["account_type"],
                            user_details,
                            len(total_projects),
                            len(total_users),
                            len(rejected_requests),
                            len(cancelled_requests),
                            len(pending_requests),
                            len(approved_requests),
                            upcoming_holidays)

    def map_error(self):
        message = "Something went wrong and your request could not be processed. Please refresh and try again."
        try:
            page_data = self.map_initial_page_data()
            page_data.state = State.Error
            page_data.message = message
            return page_data
        except:
            user_details = PublicUser(int(session["_user_id"]),
                                      None,
                                      session["account_type"],
                                      None,
                                      None,
                                      None)

            return HomePageData(State.Error,
                                message,
                                session["account_type"],
                                user_details,
                                0,
                                0,
                                0,
                                0,
                                0,
                                0,
                                [])
