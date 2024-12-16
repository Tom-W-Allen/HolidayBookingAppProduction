from datetime import datetime, date
from common.DateFunctions import get_valid_weekdays
from domains.request.models.Request import Request
from domains.request.models.RequestValidationDetails import RequestValidationDetails
from common.enums.State import State
from common.enums.RequestStatus import RequestStatus
from common.DateFunctions import find_overlapping_dates
from domains.request.RequestRepositoryInterface import IRequestRepository
from persistence.Database import Database

from common.DateFunctions import format_database_date


class RequestRepository(IRequestRepository):
    def __init__(self, database: Database):
        super().__init__(database)
        self._database = database

    def validate_request(self, start_date: str, end_date: str, user_id: int) -> RequestValidationDetails:

        state = State.Error
        valid_holidays = []

        if start_date == '' or end_date == '':
            message = "Please select a date from both fields."
            return RequestValidationDetails(state, message, valid_holidays)

        converted_start_date = format_database_date(start_date)
        converted_end_date = format_database_date(end_date)

        today = datetime(date.today().year, date.today().month, date.today().day)

        if converted_start_date <= today or converted_end_date <= today:
            message = "All days in the requested range must be a future date."

        elif converted_start_date > converted_end_date:
            message = "End date must be after start date."

        # Performance will drop if a huge date range in chosen as get_valid_weekdays will check each day in range to
        # validate whether it is a weekday or not. However, with a maximum of 25 holidays per employee, a contiguous
        # range of more than 5 full weeks will always be above their allowance anyway.
        elif (converted_end_date - converted_start_date).days > 40:
            message = ("The number of requested days exceeds your remaining balance. "
                       "Please choose a smaller range.")

        else:
            valid_holidays = get_valid_weekdays(converted_start_date, converted_end_date)
            remaining_holidays = self.get_remaining_holidays(user_id)
            pending_holidays = self.get_pending_holidays(user_id)

            pending_and_approved_requests = self.get_live_request_history(user_id)

            overlapping = False
            index = 0
            while not overlapping and index < len(pending_and_approved_requests):
                request = pending_and_approved_requests[index]

                overlap_check = find_overlapping_dates(converted_start_date,
                                                       converted_end_date,
                                                       request.start_date,
                                                       request.end_date)
                if len(overlap_check) > 0:
                    overlapping = True
                else:
                    index += 1

            if overlapping:
                message = ("Your chosen range overlaps with either your pending or approved holidays.\nPlease review "
                           "your previously requested holidays and select a new range which does not overlap.")
                return RequestValidationDetails(state, message, valid_holidays)

            if len(valid_holidays) < 1:
                message = "No weekdays selected, Saturdays and Sundays do not detract from holiday time."

            elif remaining_holidays - pending_holidays - len(valid_holidays) <= 0:
                message = ("The number of requested days exceeds your remaining balance "
                           "(including requests pending approval). "
                           "Please choose a smaller range.")

            else:
                reformatted_start_date = f"{valid_holidays[0].day}-{valid_holidays[0].month}-{valid_holidays[0].year}"
                reformatted_end_date = f"{valid_holidays[-1].day}-{valid_holidays[-1].month}-{valid_holidays[-1].year}"

                state = State.Warning
                message = (f"You are about to book {len(valid_holidays)} day(s) off between "
                           f"{reformatted_start_date} and {reformatted_end_date}. Please click 'confirm to proceed.'")

        return RequestValidationDetails(state, message, valid_holidays)

    def create_request(self, start_date: str, end_date: str, employee_id: int, approver: int, total_holidays: int):

        top_id = self._database.query_database("SELECT request_id FROM requests ORDER BY request_id DESC",
                                               limit=1)

        record_id = 1 if len(top_id) < 1 else int(top_id[0][0]) + 1
        self._database.query_database("INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?, ?)",
                                      arguments=
                                      [str(record_id),
                                       str(start_date),
                                       str(end_date),
                                       str(employee_id),
                                       str(approver),
                                       "pending",
                                       str(total_holidays)])


    def get_requests_for_approval(self, manager_id: int) -> "list[Request]":

        results = self._database.query_database("SELECT requests.request_id, users.first_name, users.surname, "
                                                "requests.start_date, requests.end_date, requests.total_holidays "
                                                "FROM requests "
                                                "JOIN users ON requests.employee_id = users.user_id "
                                                "WHERE requests.approver_id = ? AND "
                                                "requests.request_status = 'pending'",
                                                arguments=[str(manager_id)])

        request_list = []

        for row in results:
            request_list.append(Request(row[0],
                                        row[1],
                                        row[2],
                                        format_database_date(row[3]),
                                        format_database_date(row[4]),
                                        row[5],
                                        'pending'))

        return request_list


    def get_requests_for_review(self, employee_id: int) -> "list[Request]":

        results = self._database.query_database("SELECT request_id, users.first_name, users.surname, "
                                                "start_date, end_date, requests.total_holidays, "
                                                "requests.request_status "
                                                "FROM requests "
                                                "LEFT JOIN users ON requests.approver_id = users.user_id "
                                                "WHERE requests.employee_id = ? "
                                                "ORDER BY request_id DESC",
                                                arguments=[str(employee_id)])

        request_list = []
        for row in results:
            request_list.append(Request(row[0],
                                        row[1],
                                        row[2],
                                        format_database_date(row[3]),
                                        format_database_date(row[4]),
                                        row[5],
                                        row[6]))

        return request_list


    def approve_request(self, request_id: int):
        days_subtracted = self._database.query_database("SELECT total_holidays, employee_id FROM requests "
                                                        "WHERE request_id = ?",
                                                        arguments=[str(request_id)])

        self._database.query_database("UPDATE requests SET request_status = 'approved' WHERE request_id = ?",
                                      arguments=[str(request_id)])

        self._database.query_database("UPDATE users SET "
                                      "holidays_remaining = holidays_remaining - ? "
                                      "WHERE user_id = ?",
                                      arguments=
                                      [str(days_subtracted[0][0]),
                                       str(days_subtracted[0][1])])

    def reject_request(self, request_id: int):
        self._database.query_database("UPDATE requests SET request_status = 'rejected' WHERE request_id = ?",
                                      arguments=[str(request_id)])


    def cancel_request(self, request_id: int):
        self._database.query_database("UPDATE requests SET request_status = 'cancelled' WHERE request_id = ?",
                                      arguments=[str(request_id)])


    def get_remaining_holidays(self, user_id: int) -> int:
        remaining_holidays = self._database.query_database("SELECT holidays_remaining FROM users WHERE "
                                                           "user_id = ?",
                                                           arguments=[str(user_id)])

        return 0 if remaining_holidays[0][0] is None else remaining_holidays[0][0]

    def get_pending_holidays(self, user_id: int) -> int:
        pending_holidays = self._database.query_database("SELECT SUM(total_holidays) FROM requests WHERE "
                                                         "employee_id = ? AND request_status = 'pending'",
                                                         arguments=[str(user_id)])

        return 0 if pending_holidays[0][0] is None else pending_holidays[0][0]


    def get_live_request_history(self, user_id: int) -> "list[Request]":

        holidays = self._database.query_database("SELECT * FROM requests WHERE employee_id = ? AND "
                                                 "request_status IN ('approved', 'pending')",
                                                 arguments=[str(user_id)])

        pending_and_approved = []

        for record in holidays:
            # Use Request to hold start and end date data
            request = Request(record[0],
                              "",
                              "",
                              format_database_date(record[1]),
                              format_database_date(record[2]),
                              0,
                              record[5])

            pending_and_approved.append(request)

        return pending_and_approved


    def get_all_requests_by_status(self, status: RequestStatus) -> "list[Request]":

        requests = self._database.query_database("SELECT request_id, start_date, end_date "
                                                 "FROM requests WHERE request_status = ?",
                                                 arguments=[str(getattr(status, 'name'))])
        all_requests = []

        for item in requests:
            request = Request(item[0],
                              "",
                              "",
                              format_database_date(item[1]),
                              format_database_date(item[2]),
                              0,
                              str(getattr(status, 'name')))

            all_requests.append(request)

        return all_requests
