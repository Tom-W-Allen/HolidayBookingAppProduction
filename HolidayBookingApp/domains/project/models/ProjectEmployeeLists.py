from domains.user.models.PublicUser import PublicUser
from domains.project.models.ProjectMember import ProjectMember


class ProjectEmployeeLists:
    def __init__(self,
                 enrolled_employees: "list[ProjectMember]",
                 available_employees: "list[PublicUser]"):
        self.enrolled_employees = enrolled_employees
        self.available_employees = available_employees
