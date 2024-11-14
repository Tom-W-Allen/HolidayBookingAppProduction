from flask import request, session
from common.enums.State import State
from domains.project.models.Project import Project
from blueprints.models.ReviewProjectPageData import ReviewProjectPageData
from domains.project.models.ProjectEmployeeLists import ProjectEmployeeLists
from domains.project.ProjectRepositoryInterface import IProjectRepository
from mappers.BaseMapper import BaseMapper


class ReviewProjectPageMapper(BaseMapper):
    def __init__(self, project_repository: IProjectRepository):
        self.project_repository = project_repository

    def map_initial_page_data(self) -> ReviewProjectPageData:

        project_list = self.get_project_list()
        selected_project = Project(0, "--", "--", "--", 0)

        return ReviewProjectPageData(str(State.Normal),
                                     None,
                                     project_list,
                                     selected_project,
                                     [],
                                     [],
                                     0,
                                     None,
                                     None,
                                     session["account_type"])

    def map_project_selection(self) -> ReviewProjectPageData:
        project_list = self.get_project_list()

        state = State.Normal
        message = None

        if int(request.form["selected project"]) == 0:
            state = State.Warning
            message = "Please select a project to continue"
            selected_project = Project(0, "--", "--", "--", 0)
            employee_lists = ProjectEmployeeLists([], [])
        else:
            selected_project = self.filter_project_list(project_list, int(request.form["selected project"]))

            employee_lists = self.get_employee_lists(selected_project)

        return ReviewProjectPageData(str(state),
                                     message,
                                     project_list,
                                     selected_project,
                                     employee_lists.enrolled_employees,
                                     employee_lists.available_employees,
                                     0,
                                     None,
                                     None,
                                     session["account_type"])

    def map_add_employee(self) -> ReviewProjectPageData:

        project_list = self.get_project_list()
        state = State.Normal
        message = None
        button_presses = int(request.form["button presses"])
        selected_employee_id = request.form["selected employee"]

        # add employee and cancel buttons are disabled until project is selected
        selected_project = self.filter_project_list(project_list, int(request.form["selected project"]))
        employee_lists = self.get_employee_lists(selected_project)

        if selected_employee_id == 0:
            state = State.Warning
            message = "Please select an employee to continue"
            button_presses = 0

        elif button_presses > 1 and request.form["choice"] == "Add":
            # user has confirmed: add employee
            self.project_repository.add_employee_to_project(int(request.form["selected employee"]),
                                                            int(request.form["selected project"]))

            # refresh dropdowns and screen
            employee_lists = self.get_employee_lists(selected_project)

            # reset button presses
            button_presses = 0

        elif request.form["choice"] == "Add":
            # ask for confirmation
            message = "Please click 'Add' again to confirm your selection."
            state = State.Information
            selected_employee_id = int(request.form["selected employee"])
        else:
            # user chose cancel: reset back to normal
            button_presses = 0

        return ReviewProjectPageData(str(state),
                                     message,
                                     project_list,
                                     selected_project,
                                     employee_lists.enrolled_employees,
                                     employee_lists.available_employees,
                                     button_presses,
                                     selected_employee_id,
                                     None,
                                     session["account_type"])

    def map_confirm_removal(self) -> ReviewProjectPageData:
        project_list = self.get_project_list()

        selected_project = self.filter_project_list(project_list, int(request.form["selected project"]))

        employee_lists = self.get_employee_lists(selected_project)

        employee_to_remove = int(request.form["remove employee"])

        return ReviewProjectPageData(str(State.Normal),
                                     None,
                                     project_list,
                                     selected_project,
                                     employee_lists.enrolled_employees,
                                     employee_lists.available_employees,
                                     0,
                                     0,
                                     employee_to_remove,
                                     session["account_type"])

    def map_remove_employee(self) -> ReviewProjectPageData:
        project_list = self.get_project_list()

        selected_project = self.filter_project_list(project_list, int(request.form["selected project"]))

        employee_lists = self.get_employee_lists(selected_project)

        if request.form["choice"] == "Remove":
            # remove employee
            self.project_repository.remove_employee_from_project(int(request.form["remove employee"]),
                                                                 int(request.form["selected project"]))
            # refresh dropdowns and screen
            employee_lists = self.get_employee_lists(selected_project)

        return ReviewProjectPageData(str(State.Normal),
                                     None,
                                     project_list,
                                     selected_project,
                                     employee_lists.enrolled_employees,
                                     employee_lists.available_employees,
                                     0,
                                     0,
                                     None,
                                     session["account_type"])

    def map_error(self) -> ReviewProjectPageData:
        try:
            project_list = self.get_project_list()
        except:
            project_list = []

        selected_project = Project(0, "--", "--", "--", 0)

        message = "Something went wrong and your request could not be processed. Please refresh and try again."

        return ReviewProjectPageData(str(State.Error),
                                     message,
                                     project_list,
                                     selected_project,
                                     [],
                                     [],
                                     0,
                                     None,
                                     None,
                                     session["account_type"])

    def get_project_list(self) -> "list[Project]":

        if session["account_type"] == 'admin':
            return self.project_repository.get_all_projects()
        elif session["account_type"] == 'manager':
            return self.project_repository.get_manager_projects(session["_user_id"])
        else:
            return self.project_repository.get_employee_projects(session["_user_id"])

    def get_employee_lists(self, project: Project) -> ProjectEmployeeLists:

        if session["account_type"] != 'basic':
            available_employees = self.project_repository.get_available_employees(project.project_id,
                                                                                  project.project_lead)

        else:
            available_employees = []

        enrolled_employees = self.project_repository.get_enrolled_employees(project.project_id,
                                                                            project.project_lead)

        return ProjectEmployeeLists(enrolled_employees, available_employees)

    def filter_project_list(self, project_list: "list[Project]", project_id: int) -> Project:
        return [x for x in project_list if x.project_id == project_id].pop()
