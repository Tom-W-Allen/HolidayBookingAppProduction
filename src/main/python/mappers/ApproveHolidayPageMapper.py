from blueprints.models.ApproveRequestPageData import ApproveRequestPageData
from flask import session, request
from common.enums.State import State
from common.enums.UserType import UserType
from domains.request.models.Request import Request
from domains.request.RequestRepositoryInterface import IRequestRepository
from domains.user.UserRepositoryInterface import IUserRepository
from mappers.BaseMapper import BaseMapper


class ApproveHolidayPageMapper(BaseMapper):
    def __init__(self, request_repository: IRequestRepository, user_repository: IUserRepository):
        self.request_repository = request_repository
        self.user_repository = user_repository

    def map_initial_page_data(self) -> ApproveRequestPageData:

        employee_list = [] if session["account_type"] != 'admin' \
            else self.user_repository.get_user_type_details(UserType.basic)
        request_list = [] if session["account_type"] == 'admin' \
            else self.request_repository.get_requests_for_approval(session["_user_id"])

        return ApproveRequestPageData(State.Normal,
                                      None,
                                      employee_list,
                                      0,
                                      request_list,
                                      None,
                                      None,
                                      session["account_type"])

    def map_admin_user_selection(self) -> ApproveRequestPageData:

        employee_list = self.user_repository.get_user_type_details(UserType.basic)

        if int(request.form["filter"]) == 0:
            state = State.Warning
            message = "Please select a user in order to approve or reject their holiday requests."
            request_list = []
            selected_user = 0
        else:
            state = State.Normal
            message = None
            request_list = self.get_requests_by_account_type(int(request.form["filter"]))
            selected_user = int(request.form["filter"])

        return ApproveRequestPageData(state,
                                      message,
                                      employee_list,
                                      selected_user,
                                      request_list,
                                      None,
                                      None,
                                      session["account_type"])

    def map_confirm_approve_or_reject_request(self) -> ApproveRequestPageData:

        user_id = session["_user_id"] if session["account_type"] != 'admin' else request.form["selected user"]

        selected_user = int(request.form["selected user"])

        employee_list = [] if session["account_type"] != 'admin' \
            else self.user_repository.get_user_type_details(UserType.basic)
        request_list = self.get_requests_by_account_type(user_id)
        approval_required = int(request.form["request id"])

        return ApproveRequestPageData(State.Normal,
                                      None,
                                      employee_list,
                                      selected_user,
                                      request_list,
                                      approval_required,
                                      request.form["choice"],
                                      session["account_type"])

    def map_approve_or_reject_request(self) -> ApproveRequestPageData:

        user_id = session["_user_id"] if session["account_type"] != 'admin' else request.form["selected user"]

        selected_user = "0" if request.form["selected user"] == "0" else int(request.form["selected user"])

        employee_list = [] if session["account_type"] != 'admin' \
            else self.user_repository.get_user_type_details(UserType.basic)

        if request.form["choice"] == "Cancel":
            request_list = self.get_requests_by_account_type(user_id)
            state = State.Normal
            message = None
        elif request.form["choice"] == "Approve":
            self.request_repository.approve_request(int(request.form["request id"]))
            request_list = self.get_requests_by_account_type(user_id)
            state = State.Success
            message = "The request has been approved."
        else:
            self.request_repository.reject_request(int(request.form["request id"]))
            request_list = self.get_requests_by_account_type(user_id)
            state = State.Success
            message = "The request has been rejected."

        return ApproveRequestPageData(state,
                                      message,
                                      employee_list,
                                      selected_user,
                                      request_list,
                                      None,
                                      None,
                                      session["account_type"])

    def map_error(self) -> ApproveRequestPageData:

        user_id = session["_user_id"] if session["account_type"] != 'admin' else "0"
        message = "Something went wrong and your request could not be processed. Please refresh and try again."

        try:
            employee_list = [] if session["account_type"] != 'admin' \
                else self.user_repository.get_user_type_details(UserType.basic)

            request_list = [] if session["account_type"] == 'admin' \
                else self.request_repository.get_requests_for_approval(user_id)
        except:
            employee_list = []
            request_list = []

        return ApproveRequestPageData(State.Error,
                                      message,
                                      employee_list,
                                      0,
                                      request_list,
                                      None,
                                      None,
                                      session["account_type"])

    def get_requests_by_account_type(self, user_id: int) -> "list[Request]":
        if session["account_type"] == 'admin':
            # admin filters by employee rather than manager
            requests = self.request_repository.get_requests_for_review(user_id)
            return [x for x in requests if x.status == 'pending']
        else:
            return self.request_repository.get_requests_for_approval(user_id)
