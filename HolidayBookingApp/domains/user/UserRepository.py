from domains.user.models.PublicUser import PublicUser
from domains.user.models.UserLoginData import UserLoginData
from domains.user.models.EditProfileValidation import EditProfileValidation
from domains.user.models.SignupValidation import SignupValidation
from domains.user.models.PasswordValidation import PasswordValidation
from common.enums.UserType import UserType
from typing import Optional
from domains.user.UserRepositoryInterface import IUserRepository
from common.enums.State import State
from datetime import datetime
from persistence.Database import Database
import hashlib


class UserRepository(IUserRepository):
    def __init__(self, database: Database):
        super().__init__(database)
        self._database = database

    def add_user(self, username: str, password: str, account_type: str, first_name: str,
                 surname: str, holidays: int, manager: Optional[int]):

        top_id = self._database.query_database("SELECT user_id FROM users ORDER BY user_id DESC",
                                               limit=1)

        record_id = 1 if len(top_id) < 1 else int(top_id[0][0]) + 1

        self._database.query_database("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                      arguments=
                                        [str(record_id),
                                         str(username),
                                         str(password),
                                         None,
                                         str(account_type),
                                         str(first_name),
                                         str(surname),
                                         str(manager) if manager is not None else manager,
                                         str(holidays),
                                         str(0)]) # No password attempts yet as account was just created

    def get_user_manager(self, user_id: int) -> int:

        value = self._database.query_database("SELECT manager FROM users WHERE user_id = ?",
                                              arguments= [str(user_id)],
                                              limit=1)

        return value[0][0] if len(value) > 0 else -1

    def get_all_users(self) -> "list[PublicUser]":

        user_details = self._database.query_database("SELECT user_id, user_name, user_role, first_name, "
                                                     "surname, manager "
                                                     "FROM users")

        user_list = []
        for user in user_details:
            user = PublicUser(user[0], user[1], user[2], user[3], user[4], user[5])

            user_list.append(user)

        return user_list

    def get_public_user_details(self, user_id: int) -> Optional[PublicUser]:

        user_details = self._database.query_database("SELECT user_id, user_name, user_role, first_name, "
                                                     "surname, manager "
                                                     "FROM users WHERE user_id = ?",
                                                     arguments=[str(user_id)])

        if len(user_details) < 1:
            return None

        user = PublicUser(user_details[0][0],
                          user_details[0][1],
                          user_details[0][2],
                          user_details[0][3],
                          user_details[0][4],
                          None if user_details[0][5] is None else int(user_details[0][5]))

        return user

    def get_user_type_details(self, user_type: UserType):

        user_details = self._database.query_database("SELECT user_id, user_name, user_role, "
                                                     "first_name, surname, manager "
                                                     "FROM users WHERE user_role = ?",
                                                     arguments= [str(user_type.name)])

        user_list = []
        for user in user_details:
            user = PublicUser(user[0], user[1], user[2], user[3], user[4], user[5])

            user_list.append(user)

        return user_list

    def get_user_login_details(self, user_name: str) -> Optional[UserLoginData]:
        details = self._database.query_database("SELECT user_id, user_password, user_role, password_attempts "
                                                "FROM users WHERE user_name = ?",
                                                arguments=[str(user_name)])

        if len(details) < 1:
            return None

        # Use reflection to convert database user_role to enum
        role = getattr(UserType, details[0][2])

        return UserLoginData(details[0][0],
                             user_name,
                             details[0][1],
                             role,
                             details[0][3])

    def check_username_exists(self, user_name: str) -> bool:

        user_name = self._database.query_database("SELECT user_name FROM users WHERE user_name = ?",
                                                  arguments=[str(user_name)])
        return len(user_name) > 0

    def update_user(self, user: PublicUser, password_updated: bool = False):
        try:
            manager = int(user.manager)
        except ValueError:
            manager = 0

        current_details = self.get_public_user_details(user.user_id)

        self._database.query_database("UPDATE users SET "
                                      "first_name = ?, "
                                      "surname = ?, "
                                      "manager = ? "
                                      "WHERE "
                                      "user_id = ?",
                                      arguments=
                                        [str(user.first_name),
                                         str(user.surname),
                                         str(manager) if manager > 0 else None,
                                         str(user.user_id)])

        # Need to hash password before updating table if it has been changed.
        if password_updated:
            new_password = self._database.query_database("SELECT password_change FROM users WHERE user_id = ?",
                                                         arguments=[str(user.user_id)])[0][0]

            self._database.query_database("UPDATE users SET "
                                          "user_password = ?,"
                                          "password_change = NULL "
                                          "WHERE user_id = ?",
                                          arguments=
                                          [str(new_password),
                                           str(user.user_id)])

            # Make sure that employees are not automatically reassigned to projects if they switch back to former
            # manager and reflect manager change in all pending requests.
            if user.account_type == 'basic' and user.manager != current_details.manager:

                today = datetime.now()
                string_today = datetime.strftime(today, "%Y-%m-%d")

                self._database.query_database("UPDATE employee_projects "
                                              "SET leave_date = ? "
                                              "WHERE employee_id = ? AND project_id IN "
                                              "(SELECT project_id FROM projects WHERE project_lead_id = ?)",
                                              arguments=
                                              [string_today,
                                               str(user.user_id),
                                               str(current_details.manager)])

                self._database.query_database("UPDATE requests SET "
                                              "approver_id = ? "
                                              "WHERE "
                                              "employee_id = ? AND request_status = 'pending'",
                                              arguments=
                                              [str(user.manager),
                                               str(user.user_id)])

    def delete_user(self, user: PublicUser):
        # As the user table has several dependencies, may need to delete records from child tables first

        if user.account_type == 'basic':
            self._database.query_database("DELETE FROM employee_projects WHERE employee_id = ?",
                                          arguments=[str(user.user_id)])

            self._database.query_database("DELETE FROM requests WHERE employee_id = ?",
                                          arguments=[str(user.user_id)])
        elif user.account_type == 'manager':
            self._database.query_database("DELETE FROM projects WHERE project_lead_id = ?",
                                          arguments=[str(user.user_id)])

            self._database.query_database("UPDATE requests SET approver_id = ? WHERE approver_id = ?",
                                          arguments=
                                          [str(None),
                                           str(user.user_id)])

            # remove manager from other user records
            self._database.query_database("UPDATE users SET manager = NULL WHERE manager = ?",
                                          arguments=[str(user.user_id)])

        # admin accounts do not link to other tables and can be deleted straight from users
        self._database.query_database("DELETE FROM users WHERE user_id = ?",
                                      arguments=[str(user.user_id)])

    def validate_edit_profile(self, proposed_details: PublicUser, password: str, confirmed_password: str) \
            -> EditProfileValidation:
        state = State.Warning
        password_changed = False

        password_validation = None

        if password != "" or confirmed_password != "":
            password_changed = True
            password_validation = self.validation_password(password, confirmed_password)

        # Problem found with password, no need to process further
        if password_validation is not None and password_validation.state == State.Warning:
            return EditProfileValidation(password_validation.state, password_validation.message)

        current_details = self.get_public_user_details(proposed_details.user_id)

        # password is either ok or has not changed
        if proposed_details.first_name == "" or proposed_details.surname == "":
            message = "First name and surname cannot be blank."
        elif proposed_details.account_type == 'basic' and int(proposed_details.manager) == 0:
            message = "Manager must be chosen from dropdown"
        elif current_details == proposed_details and not password_changed:
            message = "No changes have been made."
        else:
            state = State.Normal
            message = None

        return EditProfileValidation(state, message)

    def validate_signup_data(self, username: str, password: str, confirmed_password: str,
                             first_name: str, surname: str) -> SignupValidation:
        state = State.Warning

        if self.check_username_exists(username):
            message = "User name already exists"
        elif username == '':
            message = "User name cannot be blank"
        elif first_name == '':
            message = "First name cannot be blank"
        elif surname == '':
            message = "Surname cannot be blank"
        else:
            password_validation = self.validation_password(password, confirmed_password)
            state = password_validation.state
            message = password_validation.message

        return SignupValidation(state, message)

    def validation_password(self, password: str, confirmed_password: str) -> PasswordValidation:
        state = State.Warning

        if password != confirmed_password:
            message = "Password and confirmed password do not match"
        elif len(password) < 10:
            message = "Password must be at least 10 characters long."
        elif len([x for x in password if x.isnumeric()]) < 1:
            message = "Password must contain at least one number"
        elif len([x for x in password if x.isalnum()]) == len(password):
            message = "Password must contain at least one special character, e.g., !, $, ?, @, etc..."
        else:
            state = State.Success
            message = None

        return PasswordValidation(state, message)

    def store_proposed_password(self, user_id: int, password: str) -> None:
        bytes_password = hashlib.sha256(password.encode())
        hash_digest = bytes_password.hexdigest()

        self._database.query_database("UPDATE users SET password_change = ? WHERE user_id = ?",
                                      arguments=
                                      [str(hash_digest),
                                       str(user_id)])


    def clear_password_change(self, user_id: int) -> None:
        self._database.query_database("UPDATE users SET password_change = NULL WHERE user_id = ?",
                                      arguments=[str(user_id)])


    def verify_password_change(self, user_id: int) -> bool:
        password_change = self._database.query_database("SELECT password_change FROM users WHERE "
                                                        "user_id = ?",
                                                        arguments=[str(user_id)])

        return password_change[0][0] is not None


    def get_password_attempts(self, user_id: int) -> int:
        password_attempts = self._database.query_database("SELECT password_attempts FROM users WHERE "
                                                          "user_id = ?",
                                                          arguments=[str(user_id)])

        return int(password_attempts[0][0])

    def update_password_attempts(self, user_id: int, new_attempts: int) -> None:
        self._database.query_database("UPDATE users SET password_attempts = ? WHERE user_id = ?",
                                      arguments=
                                      [str(new_attempts),
                                       str(user_id)])

