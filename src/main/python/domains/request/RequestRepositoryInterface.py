from domains.request.models.Request import Request
from domains.request.models.RequestValidationDetails import RequestValidationDetails
from common.enums.RequestStatus import RequestStatus
from persistence.Database import Database


# For details on informal Python interfaces, see (Murphy, 2024).
class IRequestRepository:
    def __init__(self, database: Database):
        self._database = database

    def validate_request(self, start_date: str, end_date: str, user_id: int) -> RequestValidationDetails:
        pass

    def create_request(self, start_date: str, end_date: str, employee_id: int, approver: int, total_holidays: int):
        pass

    def get_requests_for_approval(self, manager_id: int) -> "list[Request]":
        pass

    def get_requests_for_review(self, employee_id: int) -> "list[Request]":
        pass

    def approve_request(self, request_id: int):
        pass

    def reject_request(self, request_id: int):
        pass

    def cancel_request(self, request_id: int):
        pass

    def get_remaining_holidays(self, user_id: int) -> int:
        pass

    def get_pending_holidays(self, user_id: int) -> int:
        pass

    def get_all_requests_by_status(self, status: RequestStatus) -> "list[Request]":
        pass
