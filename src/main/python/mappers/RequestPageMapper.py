from flask import session, request
from blueprints.models.RequestPageData import BaseRequestPageData, FullRequestPageData
from common.enums.UserType import UserType
from domains.request.models.RequestDates import RequestDates
from common.enums.State import State
from datetime import datetime
from common.DateFunctions import get_valid_weekdays
from domains.request.RequestRepositoryInterface import IRequestRepository
from domains.user.UserRepositoryInterface import IUserRepository
from mappers.BaseMapper import BaseMapper


class RequestPageMapper(BaseMapper):
    def __init__(self, user_repository: IUserRepository, request_repository: IRequestRepository):
        self.user_repository = user_repository
        self.request_repository = request_repository

    def map_initial_page_data(self) -> FullRequestPageData:
        base_page_data = self.get_base_request_page_data(session["_user_id"])

        return FullRequestPageData(str(State.Normal),
                                   None,
                                   base_page_data.remaining_holidays,
                                   base_page_data.pending_holidays,
                                   session["account_type"],
                                   int(session["_user_id"]),
                                   None,
                                   base_page_data.basic_users,
                                   base_page_data.request_list,
                                   None,
                                   base_page_data.manager,
                                   base_page_data.base_user)

    def map_admin_selection(self) -> FullRequestPageData:

        if request.form["filter"] == "--":
            state = State.Warning
            message = "Please select a user to make a holiday request on their behalf."
            user_id = int(session["_user_id"])
        else:
            state = State.Normal
            message = None
            user_id = int(request.form["filter"])

        base_page_data = self.get_base_request_page_data(user_id)

        return FullRequestPageData(str(state),
                                   message,
                                   base_page_data.remaining_holidays,
                                   base_page_data.pending_holidays,
                                   session["account_type"],
                                   user_id,
                                   None,
                                   base_page_data.basic_users,
                                   base_page_data.request_list,
                                   None,
                                   base_page_data.manager,
                                   base_page_data.base_user)

    def map_date_submission(self) -> FullRequestPageData:

        # Admin user has not selected another user from the dropdown
        if session["account_type"] == 'admin' and (session["_user_id"] == request.form["Selected User"]):
            user_id = session["_user_id"]
            state = State.Warning
            message = "Please select a user to make a holiday request on their behalf."
            request_dates = None

            base_page_data = self.get_base_request_page_data(user_id)
        else:

            user_id = int(session["_user_id"]) if session["account_type"] != "admin" \
                                               else int(request.form["Selected User"])

            base_page_data = self.get_base_request_page_data(user_id)

            validation_results = self.request_repository.validate_request(request.form["Start Date"],
                                                                          request.form["End Date"],
                                                                          user_id)
            state = validation_results.state
            message = validation_results.message

            if validation_results.state == State.Error:
                request_dates = None
            else:
                request_dates = RequestDates(request.form["Start Date"],
                                             request.form["End Date"],
                                             validation_results.valid_holidays[0],
                                             validation_results.valid_holidays[-1],
                                             validation_results.valid_holidays)

        return FullRequestPageData(state,
                                   message,
                                   base_page_data.remaining_holidays,
                                   base_page_data.pending_holidays,
                                   session["account_type"],
                                   user_id,
                                   request_dates,
                                   base_page_data.basic_users,
                                   base_page_data.request_list,
                                   None,
                                   base_page_data.manager,
                                   base_page_data.base_user)

    def map_date_confirmation(self) -> FullRequestPageData:

        user_id = int(session["_user_id"]) if session["account_type"] != "admin" else int(request.form["Selected User"])

        base_page_data = self.get_base_request_page_data(user_id)
        message = None
        state = State.Normal

        if request.form["choice"] == "Confirm":
            approver = self.user_repository.get_user_manager(user_id)
            converted_start_date = datetime.strptime(request.form["Start Date"], "%Y-%m-%d")
            converted_end_date = datetime.strptime(request.form["End Date"], "%Y-%m-%d")

            valid_weekdays = get_valid_weekdays(converted_start_date, converted_end_date)

            # ensure date format is stored in the database the same as it is in the html form
            string_start_date = datetime.strftime(valid_weekdays[0], "%Y-%m-%d")
            string_end_date = datetime.strftime(valid_weekdays[-1], "%Y-%m-%d")

            self.request_repository.create_request(string_start_date,
                                                   string_end_date,
                                                   user_id,
                                                   approver,
                                                   len(valid_weekdays))

            message = "Thank you, your request has been submitted."
            state = State.Success
            base_page_data = self.get_base_request_page_data(user_id)

        return FullRequestPageData(str(state),
                                   message,
                                   base_page_data.remaining_holidays,
                                   base_page_data.pending_holidays,
                                   session["account_type"],
                                   user_id,
                                   None,
                                   base_page_data.basic_users,
                                   base_page_data.request_list,
                                   None,
                                   base_page_data.manager,
                                   base_page_data.base_user)

    def map_confirm_cancel(self) -> FullRequestPageData:
        user_id = int(session["_user_id"]) if session["account_type"] != "admin" else int(request.form["Selected User"])
        base_page_data = self.get_base_request_page_data(user_id)

        request_list = self.request_repository.get_requests_for_review(user_id)
        request_to_remove = int(request.form["id"])

        return FullRequestPageData(str(State.Normal),
                                   None,
                                   base_page_data.remaining_holidays,
                                   base_page_data.pending_holidays,
                                   session["account_type"],
                                   user_id,
                                   None,
                                   base_page_data.basic_users,
                                   request_list,
                                   request_to_remove,
                                   base_page_data.manager,
                                   base_page_data.base_user)

    def map_cancel_request(self) -> FullRequestPageData:
        self.request_repository.cancel_request(int(request.form["id"]))
        message = "The request has successfully been cancelled"

        # Refresh view
        user_id = int(session["_user_id"]) if session["account_type"] != "admin" else int(request.form["Selected User"])
        base_page_data = self.get_base_request_page_data(user_id)
        request_list = self.request_repository.get_requests_for_review(user_id)

        return FullRequestPageData(str(State.Success),
                                   message,
                                   base_page_data.remaining_holidays,
                                   base_page_data.pending_holidays,
                                   session["account_type"],
                                   user_id,
                                   None,
                                   base_page_data.basic_users,
                                   request_list,
                                   None,
                                   base_page_data.manager,
                                   base_page_data.base_user)

    def map_error(self) -> FullRequestPageData:
        try:
            account_type = session["account_type"]
            user_id = session["_user_id"]
        except Exception:
            account_type = UserType.basic
            user_id = 0

        message = "Something went wrong and your request could not be processed. Please refresh and try again."

        return FullRequestPageData(str(State.Error),
                                   message,
                                   0,
                                   0,
                                   account_type,
                                   user_id,
                                   None,
                                   [],
                                   [],
                                   None,
                                   None,
                                   user_id)

    def get_base_request_page_data(self, user_id: int) -> BaseRequestPageData:
        basic_users = []
        manager = self.user_repository.get_public_user_details(user_id).manager
        base_user = int(session["_user_id"])

        request_list = self.request_repository.get_requests_for_review(user_id)

        if session["account_type"] == 'admin':
            basic_users = self.user_repository.get_user_type_details(UserType.basic)

        unprocessed_holidays = self.request_repository.get_remaining_holidays(user_id)
        pending_holidays = self.request_repository.get_pending_holidays(user_id)
        remaining_holidays = unprocessed_holidays - pending_holidays

        return BaseRequestPageData(remaining_holidays, pending_holidays, basic_users, request_list, manager, base_user)
