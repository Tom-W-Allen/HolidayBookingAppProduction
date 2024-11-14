from datetime import datetime, date
from common.DateFunctions import get_valid_weekdays, find_overlapping_dates
from domains.project.models.Project import Project
from domains.project.models.ProjectValidationDetails import ProjectValidationDetails
from domains.user.models.PublicUser import PublicUser
from common.enums.State import State
from domains.project.models.ProjectMember import ProjectMember
from domains.project.ProjectRepositoryInterface import IProjectRepository
from persistence.Database import Database


class ProjectRepository(IProjectRepository):
    def __init__(self, connection_string: str, database: Database):
        super().__init__(connection_string, database)
        self._database = database

    def validate_project_dates(self, start_date: str, end_date: str, project_name: str) -> ProjectValidationDetails:

        message = None
        state = State.Warning

        if project_name == '':
            message = "Project name cannot be blank"
            return ProjectValidationDetails(state, message)

        elif self.find_project_name(project_name):
            message = "Project name is already in use"
            return ProjectValidationDetails(state, message)

        if start_date == '' or end_date == '':
            message = "Please select a date from both fields."
            return ProjectValidationDetails(state, message)

        converted_start_date = datetime.strptime(start_date, "%Y-%m-%d")
        converted_end_date = datetime.strptime(end_date, "%Y-%m-%d")

        today = datetime(date.today().year, date.today().month, date.today().day)

        if converted_start_date > converted_end_date:
            message = "End date must be after start date."
        elif converted_start_date <= today or converted_end_date <= today:
            message = "All dates in selected range must be after the current date."
        else:
            # If difference between start and end date is greater than 2, date range must extend beyond weekend and
            # include valid weekdays. Only need to check if weekdays are included if there are 2 or fewer project days
            # assigned.
            if (converted_end_date - converted_start_date).days < 3:
                valid_project_days = get_valid_weekdays(converted_start_date, converted_end_date)

                if len(valid_project_days) < 1:
                    message = "No weekdays selected, projects must be completed in work hours."
                else:
                    state = State.Success
            else:
                state = State.Success

        return ProjectValidationDetails(state, message)

    def create_project(self, project_name: str, start_date: str, end_date: str, project_lead: int):

        # Employee project records are not deleted, only updated. Therefore, need to make sure that id is unique
        # for both projects and employee projects tables, otherwise employees may accidentally get assigned
        # to new projects automatically.

        projects_top_id = self._database.query_database("SELECT project_id FROM projects "
                                                        "ORDER BY project_id DESC",
                                                        limit=1)

        employee_projects_top_id = self._database.query_database("SELECT project_id FROM employee_projects "
                                                                 "ORDER BY project_id DESC",
                                                                 limit=1)

        if len(projects_top_id) > 0 and len(employee_projects_top_id) == 0:
            top_id = projects_top_id[0][0]
        elif len(projects_top_id) == 0 and len(employee_projects_top_id) > 0:
            top_id = employee_projects_top_id[0][0]
        elif len(projects_top_id) == 0 and len(employee_projects_top_id) == 0:
            top_id = 0
        else:
            # Records in both tables so take the larger value
            top_id = max(projects_top_id[0][0], employee_projects_top_id[0][0])

        record_id = top_id + 1

        self._database.query_database("INSERT INTO projects VALUES (?, ?, ?, ?, ?)",
                                      arguments=
                                      [str(record_id),
                                       str(project_name),
                                       str(start_date),
                                       str(end_date),
                                       str(project_lead)])

    def get_all_projects(self) -> "list[Project]":

        projects = self._database.query_database("SELECT project_id, project_name, start_date, end_date, "
                                                 "project_lead_id FROM projects")

        project_list = []
        for i in range(0, len(projects)):
            converted_start_date = datetime.strptime(projects[i][2], "%Y-%m-%d")
            converted_end_date = datetime.strptime(projects[i][3], "%Y-%m-%d")

            project_list.append(Project(projects[i][0],
                                        projects[i][1],
                                        converted_start_date,
                                        converted_end_date,
                                        projects[i][4]))

        return project_list


    def get_manager_projects(self, manager_id: int) -> "list[Project]":
        projects = self._database.query_database("SELECT project_id, project_name, start_date, end_date "
                                                 "FROM projects"
                                                 " WHERE project_lead_id = ?",
                                                 arguments=[str(manager_id)])

        project_list = []
        for i in range(0, len(projects)):
            converted_start_date = datetime.strptime(projects[i][2], "%Y-%m-%d")
            converted_end_date = datetime.strptime(projects[i][3], "%Y-%m-%d")

            project_list.append(Project(projects[i][0],
                                        projects[i][1],
                                        converted_start_date,
                                        converted_end_date,
                                        manager_id))

        return project_list


    def get_employee_projects(self, employee_id: int) -> "list[Project]":
        today = datetime.now()
        string_today = datetime.strftime(today, "%Y-%m-%d")

        projects = self._database.query_database("SELECT projects.project_id, projects.project_name, "
                                                 "projects.start_date, projects.end_date, projects.project_lead_id "
                                                 "FROM projects "
                                                 "JOIN employee_projects ON "
                                                 "projects.project_id = employee_projects.project_id "
                                                 "WHERE employee_projects.employee_id = ? AND "
                                                 "employee_projects.leave_date > ?",
                                                 arguments=
                                                 [str(employee_id),
                                                  string_today])

        project_list = []
        for i in range(0, len(projects)):
            converted_start_date = datetime.strptime(projects[i][2], "%Y-%m-%d")
            converted_end_date = datetime.strptime(projects[i][3], "%Y-%m-%d")

            project_list.append(Project(projects[i][0],
                                        projects[i][1],
                                        converted_start_date,
                                        converted_end_date,
                                        projects[i][4]))

        return project_list


    def get_available_employees(self, project_id: int, manager_id: int) -> "list[PublicUser]":
        today = datetime.now()
        string_today = datetime.strftime(today, "%Y-%m-%d")

        # Find users who have the project lead as their manager and do not have employee_project records with
        # a leave date later than today (which indicates they are currently enrolled on the project).
        available_employees = self._database.query_database(
            "SELECT user_id, user_name, user_role, first_name, surname, manager "
            "FROM users AS u1 "
            "WHERE "
            "manager = ? AND "
            "NOT EXISTS (SELECT * FROM employee_projects WHERE "
            "employee_id = u1.user_id AND project_id = ? AND leave_date > ?)",
            arguments=
            [str(manager_id),
             str(project_id),
             string_today])

        available_employees_list = []
        for employee in available_employees:
            selected_employee = PublicUser(employee[0],
                                           employee[1],
                                           employee[2],
                                           employee[3],
                                           employee[4],
                                           employee[5])
            available_employees_list.append(selected_employee)

        return available_employees_list


    def get_enrolled_employees(self, project_id: int, manager_id: int) -> "list[ProjectMember]":
        today = datetime.now()
        string_today = datetime.strftime(today, "%Y-%m-%d")

        # Find users who have the project lead as their manager and have employee_project records with
        # a leave date later than today (which indicates they are currently enrolled on the project).
        enrolled_employees = self._database.query_database(
            "SELECT user_id, user_name, user_role, first_name, surname "
            "FROM users AS u1 "
            "WHERE "
            "manager = ? AND "
            "EXISTS (SELECT * FROM employee_projects WHERE "
            "employee_id = u1.user_id AND project_id = ? AND leave_date > ?)",
            arguments=
            [str(manager_id),
             str(project_id),
             string_today])

        enrolled_employees_list = []
        for employee in enrolled_employees:
            overlapping_holiday = self.get_project_overlap_holidays(employee[0], project_id)

            selected_employee = ProjectMember(employee[0],
                                              employee[1],
                                              employee[2],
                                              employee[3],
                                              employee[4],
                                              overlapping_holiday)

            enrolled_employees_list.append(selected_employee)

        return enrolled_employees_list


    def add_employee_to_project(self, user_id: int, project_id: int):

        # get the default dates for project based on the project table
        dates = self._database.query_database("SELECT start_date, end_date FROM projects WHERE "
                                              "project_id = ?",
                                              arguments=[str(project_id)])

        # Check if an employee_project history record already exists
        pre_existing_record = self._database.query_database("SELECT * FROM employee_projects WHERE "
                                                            "employee_id = ? AND project_id = ?",
                                                            arguments=
                                                            [str(user_id),
                                                             str(project_id)])

        if len(pre_existing_record) > 0:
            today = datetime.now()
            string_today = datetime.strftime(today, "%Y-%m-%d")

            # If record exists, just update the join and leave dates
            self._database.query_database("UPDATE employee_projects SET join_date = ?, leave_date = ? WHERE "
                                          "employee_id = ? AND project_id = ?",
                                          arguments=
                                          [string_today,
                                           dates[0][1],  # default leave date
                                           str(user_id),
                                           str(project_id)])
        else:
            # If record does not exist, create a new one.
            self._database.query_database("INSERT INTO employee_projects VALUES (?, ?, ? ,?)",
                                          arguments=
                                          [str(project_id),
                                           str(user_id),
                                           str(dates[0][0]),  # default start date
                                           str(dates[0][1])])  # default leave date


    def remove_employee_from_project(self, employee_id: int, project_id: int):
        today = datetime.now()
        string_today = datetime.strftime(today, "%Y-%m-%d")

        self._database.query_database("UPDATE employee_projects "
                                      "SET leave_date = ? WHERE employee_id = ? AND project_id = ?",
                                      arguments=
                                      [string_today,
                                       str(employee_id),
                                       str(project_id)])


    def find_project_name(self, project_name: str) -> bool:

        name = self._database.query_database("SELECT * FROM projects WHERE project_name = ? LIMIT 1",
                                             arguments=[str(project_name)])

        return len(name) > 0


    def get_project_overlap_holidays(self, user_id: int, project_id: int) -> "list[datetime]":

        project_dates = self._database.query_database("SELECT start_date, end_date FROM projects WHERE "
                                                      "project_id = ? LIMIT 1",
                                                      arguments=[str(project_id)])

        converted_project_start_date = datetime.strptime(project_dates[0][0], "%Y-%m-%d")
        converted_project_end_date = datetime.strptime(project_dates[0][1], "%Y-%m-%d")

        approved_holidays = self._database.query_database("SELECT start_date, end_date "
                                                          "FROM requests "
                                                          "WHERE employee_id = ? AND request_status = 'approved'",
                                                          arguments=[str(user_id)])

        overlap_holidays = []

        for holiday_range in approved_holidays:
            converted_start_date = datetime.strptime(holiday_range[0], "%Y-%m-%d")
            converted_end_date = datetime.strptime(holiday_range[1], "%Y-%m-%d")

            overlap_holidays.extend(find_overlapping_dates(converted_start_date,
                                                           converted_end_date,
                                                           converted_project_start_date,
                                                           converted_project_end_date))

        return overlap_holidays

