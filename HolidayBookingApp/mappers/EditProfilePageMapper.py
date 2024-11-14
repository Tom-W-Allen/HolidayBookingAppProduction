from flask import session, request
from blueprints.models.EditProfilePageData import EditProfilePageData
from common.enums.State import State
from common.enums.UserType import UserType
from domains.user.models.PublicUser import PublicUser
from domains.user.models.ManagerAccountDetails import ManagerAccountDetails
from domains.project.ProjectRepositoryInterface import IProjectRepository
from domains.request.RequestRepositoryInterface import IRequestRepository
from domains.user.UserRepositoryInterface import IUserRepository
from mappers.BaseMapper import BaseMapper


class EditProfilePageMapper(BaseMapper):
    def __init__(self,
                 user_repository: IUserRepository,
                 request_repository: IRequestRepository,
                 project_repository: IProjectRepository):
        self.user_repository = user_repository
        self.request_repository = request_repository
        self.project_repository = project_repository

    def map_initial_page_data(self) -> EditProfilePageData:

        employee_list = [] if session["account_type"] != 'admin' else self.user_repository.get_all_users()

        manager_list = [] if session["account_type"] != 'basic' \
            else self.user_repository.get_user_type_details(UserType.manager)

        user_details = self.user_repository.get_public_user_details(session["_user_id"])

        return EditProfilePageData(State.Normal,
                                   None,
                                   session["account_type"],
                                   user_details.user_id,
                                   employee_list,
                                   user_details,
                                   manager_list,
                                   False,
                                   0,
                                   int(session["_user_id"]),
                                   user_details.manager)

    def map_select_user(self) -> EditProfilePageData:
        employee_list = self.user_repository.get_all_users()

        user_details = self.user_repository.get_public_user_details(int(request.form["filter"]))

        manager_account_details = self.get_account_and_manager_details(user_details.user_id)

        manager_list = [] if manager_account_details.account_type != 'basic' \
            else self.user_repository.get_user_type_details(UserType.manager)

        return EditProfilePageData(State.Normal,
                                   None,
                                   session["account_type"],
                                   user_details.user_id,
                                   employee_list,
                                   user_details,
                                   manager_list,
                                   False,
                                   0,
                                   int(session["_user_id"]),
                                   user_details.manager)

    def map_delete_user(self) -> EditProfilePageData:
        user_id = int(request.form["selected user"])

        # Admin may be deleting another admin or manager's account (in which case there is no manager list).
        # Determine manager value based on what is selected in the user selection filter.
        manager_account_details = self.get_account_and_manager_details(user_id)

        manager_list = [] if manager_account_details.account_type != 'basic' \
            else self.user_repository.get_user_type_details(UserType.manager)

        user_details = self.user_repository.get_public_user_details(user_id)

        if request.form["choice"] == 'Cancel':
            state = State.Normal
            message = None
            button_presses = 0

        elif int(request.form["delete button presses"]) == 1:
            state = State.Warning

            # deleting a manager will affect projects and users - need to provide admin with more information than
            # standard user or another admin
            if user_details.account_type == 'manager':
                associated_projects = self.project_repository.get_manager_projects(user_details.user_id)

                message = (f"You are about to delete the MANAGER account of {user_details.user_name}. "
                           f"Deleting this account will delete all associated projects "
                           f"({len(associated_projects)} in total).\n"
                           f"Users associated with this manager will also need to edit their profile to select "
                           f"a new manager. "
                           f"Please press 'Delete Account' again to confirm.")

            elif user_details.account_type == 'admin':
                message = (f"You are about to delete the ADMIN account of {user_details.user_name}, "
                           f"please press 'Delete Account' again to confirm.")
            else:
                message = (f"You are about to delete the BASIC account of {user_details.user_name}, "
                           f"please press 'Delete Account' again to confirm.")

            button_presses = 1
        else:
            user_name = self.user_repository.get_public_user_details(int(request.form["selected user"])).user_name
            
            self.user_repository.delete_user(user_details)

            # change user details to current admin
            user_details = self.user_repository.get_public_user_details(session["_user_id"])
            
            state = State.Success
            message = f"You successfully deleted the account with username: {user_name}."
            button_presses = 0
            # When deleted, view will revert back to user who is an admin - make sure manager list
            # is empty, so it is not displayed on screen
            manager_list = []

        # Wait until end of processing to get full list of employees in order to account for one being deleted.
        employee_list = self.user_repository.get_all_users()

        return EditProfilePageData(state,
                                   message,
                                   session["account_type"],
                                   user_details.user_id,
                                   employee_list,
                                   user_details,
                                   manager_list,
                                   False,
                                   button_presses,
                                   int(session["_user_id"]),
                                   user_details.manager)

    def map_confirm_changes(self) -> EditProfilePageData:
        employee_list = [] if session["account_type"] != 'admin' else self.user_repository.get_all_users()

        user_id = int(request.form["selected user"])

        # Admin may be editing their own account (in which case there is no manager list) or editing on behalf of
        # another user. Determine manager value based on what is selected in the user selection filter.
        manager_account_details = self.get_account_and_manager_details(user_id)

        manager_list = [] if manager_account_details.account_type != 'basic' \
            else self.user_repository.get_user_type_details(UserType.manager)

        user_details = PublicUser(user_id,
                                  request.form["user name"],
                                  manager_account_details.account_type,
                                  request.form["first name"],
                                  request.form["surname"],
                                  manager_account_details.manager)

        validation = self.user_repository.validate_edit_profile(user_details,
                                                                request.form["password"],
                                                                request.form["password confirmation"])

        # Invalid inputs, reset form
        if validation.state == State.Warning:
            user_details = self.user_repository.get_public_user_details(user_id)
            manager = user_details.manager
            approval_required = False
        else:
            # set manager as 0 if request is for manager or admin
            manager = 0 if "manager" not in request.form.keys() else int(request.form["manager"])
            approval_required = True

            # Password has been validated, store it in table to confirm change
            if request.form["password"] != "":
                self.user_repository.store_proposed_password(user_id, request.form["password"])

        return EditProfilePageData(validation.state,
                                   validation.message,
                                   session["account_type"],
                                   user_details.user_id,
                                   employee_list,
                                   user_details,
                                   manager_list,
                                   approval_required,
                                   0,
                                   int(session["_user_id"]),
                                   manager)

    def map_execute_changes(self) -> EditProfilePageData:
        user_id = int(request.form["selected user"])

        manager_account_details = self.get_account_and_manager_details(user_id)

        manager_list = [] if manager_account_details.account_type != 'basic' \
            else self.user_repository.get_user_type_details(UserType.manager)

        form_data = PublicUser(user_id,
                               request.form["user name"],
                               manager_account_details.account_type,
                               request.form["first name"],
                               request.form["surname"],
                               manager_account_details.manager)

        if request.form["choice"] == "Cancel":
            state = State.Normal
            message = None
            self.user_repository.clear_password_change(user_id)
        else:
            password_changed = self.user_repository.verify_password_change(user_id)
            self.user_repository.update_user(form_data, password_changed)
            message = "Your account details have been successfully updated"
            state = State.Success

        # Reset form details
        user_details = self.user_repository.get_public_user_details(user_id)
        employee_list = [] if session["account_type"] != 'admin' else self.user_repository.get_all_users()

        return EditProfilePageData(state,
                                   message,
                                   session["account_type"],
                                   user_id,
                                   employee_list,
                                   user_details,
                                   manager_list,
                                   False,
                                   0,
                                   int(session["_user_id"]),
                                   user_details.manager)

    def map_error(self) -> EditProfilePageData:
        try:
            employee_list = [] if session["account_type"] != 'admin' else self.user_repository.get_all_users()

            manager_list = [] if session["account_type"] != 'basic' \
                else self.user_repository.get_user_type_details(UserType.manager)

            user_details = self.user_repository.get_public_user_details(session["_user_id"])

            user_id = user_details.user_id

            self.user_repository.clear_password_change(user_id)

        except Exception:
            user_id = session["_user_id"]
            employee_list = []
            manager_list = []
            user_details = PublicUser(user_id,
                                      None,
                                      session["account_type"],
                                      None,
                                      None,
                                      None)

        message = "Something went wrong and your request could not be processed. Please refresh and try again."
        session["refresh_page"] = "yes"
        return EditProfilePageData(State.Error,
                                   message,
                                   session["account_type"],
                                   user_id,
                                   employee_list,
                                   user_details,
                                   manager_list,
                                   False,
                                   0,
                                   int(session["_user_id"]),
                                   0)

    def get_account_and_manager_details(self, user_id: int) -> ManagerAccountDetails:
        if session["account_type"] == 'admin':
            proxy_user_details = self.user_repository.get_public_user_details(user_id)
            account_type = proxy_user_details.account_type
            if account_type != 'basic':
                manager = 0
            elif "manager" not in request.form.keys():
                manager = None if proxy_user_details.manager is None else int(proxy_user_details.manager)
            else:
                manager = int(request.form["manager"])
        elif session["account_type"] == 'manager':
            account_type = session["account_type"]
            manager = 0
        else:
            account_type = session["account_type"]
            manager = int(request.form["manager"])

        return ManagerAccountDetails(manager, account_type)
