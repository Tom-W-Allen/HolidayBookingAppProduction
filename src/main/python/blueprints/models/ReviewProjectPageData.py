from domains.project.models.Project import Project
from domains.user.models.PublicUser import PublicUser
from domains.project.models.ProjectMember import ProjectMember
from blueprints.models.BasePageData import BasePageData
from typing import Optional


class ReviewProjectPageData(BasePageData):
    def __init__(self,
                 state: str,
                 message: Optional[str],
                 project_list: "list[Project]",
                 selected_project: Project,
                 enrolled_employees: "list[ProjectMember]",
                 available_employees: "list[PublicUser]",
                 add_employee_button_presses: int,
                 selected_employee_id: Optional[int],
                 remove_employee: Optional[int],
                 account_type: str,
                 redirect=None,
                 logout_presses=0):
        super().__init__(redirect, logout_presses)
        self.state = state
        self.message = message
        self.project_list = project_list
        self.selected_project = selected_project
        self.enrolled_employees = enrolled_employees
        self.available_employees = available_employees
        self.add_employee_button_presses = add_employee_button_presses
        self.selected_employee_id = selected_employee_id
        self.remove_employee = remove_employee
        self.account_type = account_type
