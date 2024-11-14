from datetime import datetime
from domains.project.models.Project import Project
from domains.project.models.ProjectValidationDetails import ProjectValidationDetails
from domains.user.models.PublicUser import PublicUser
from domains.project.models.ProjectMember import ProjectMember
from persistence.Database import Database


# For details on informal Python interfaces, see (Murphy, 2024).
class IProjectRepository:
    def __init__(self, connection_string: str, database: Database):
        self._connection_string = connection_string
        self._database = database

    def validate_project_dates(self, start_date: str, end_date: str, project_name: str) -> ProjectValidationDetails:
        pass

    def create_project(self, project_name: str, start_date: str, end_date: str, project_lead: int):
        pass

    def get_all_projects(self) -> "list[Project]":
        pass

    def get_manager_projects(self, manager_id: int) -> "list[Project]":
        pass

    def get_employee_projects(self, employee_id: int) -> "list[Project]":
        pass

    def get_available_employees(self, project_id: int, manager_id: int) -> "list[PublicUser]":
        pass

    def get_enrolled_employees(self, project_id: int, manager_id: int) -> "list[ProjectMember]":
        pass

    def add_employee_to_project(self, user_id: int, project_id: int):
        pass

    def remove_employee_from_project(self, employee_id: int, project_id: int):
        pass

    def find_project_name(self, project_name: str) -> bool:
        pass

    def get_project_overlap_holidays(self, user_id: int, project_id: int) -> "list[datetime]":
        pass


