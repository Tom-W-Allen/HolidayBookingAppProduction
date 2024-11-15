from blueprints.models.LoginPageData import LoginPageData
from domains.user.UserRepositoryInterface import IUserRepository


from flask import request, session
from common.enums.State import *
from flask_login import login_user
from domains.user.models.UserSession import UserSession
import hashlib


class LoginPageMapper:

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def map_initial_page_data(self) -> LoginPageData:
        return LoginPageData(None,
                             State.Normal,
                             None,
                             False)

    def map_login(self) -> LoginPageData:
        state = State.Normal
        login_redirect = None
        message = None

        user_details = self.user_repository.get_user_login_details(request.form["User Name"])

        if user_details.password_attempts == 3:
            message = ("You have entered an incorrect password three times. Please click on the link below to "
                       "reset your password with the email that you used to register.")
            return LoginPageData(login_redirect,
                                 State.Warning,
                                 message,
                                 False)

        # Since passwords are stored in the database in a hashed form, need to convert the password provided by the
        # user to bytes so that hashlib's sha256 method can get its hash digest (Python, 2024a; W3 Schools, 2024).
        bytes_password = hashlib.sha256(request.form["Password"].encode())

        hash_digest = bytes_password.hexdigest()

        if user_details is not None and (user_details.password == hash_digest):
            # Password has been entered correctly in fewer than three attempts. Reset to zero.
            self.user_repository.update_password_attempts(user_details.user_id, 0)

            login_user_object = UserSession(user_details.user_id)
            login_user(login_user_object)

            session["logged_in"] = [str(user_details.user_id)]
            session["account_type"] = getattr(user_details.user_role, "name")
            session["refresh_page"] = "no"
            # To avoid open redirect vulnerability, always redirect to home page regardless of url stored in
            # "next".
            login_redirect = '/'
        else:
            state = State.Warning
            message = "Incorrect user name or password (Warning: 3 incorrect password attempts will lock your account)"

        if user_details is not None:
            # Username is valid, but password has been entered incorrectly. Increment attempts by one.
            current_attempts = self.user_repository.get_password_attempts(user_details.user_id)
            self.user_repository.update_password_attempts(user_details.user_id, current_attempts + 1)

        return LoginPageData(login_redirect,
                             state,
                             message,
                             False)

    def map_sign_up(self) -> LoginPageData:
        return LoginPageData(None,
                             State.Normal,
                             None,
                             True)

    def map_sign_up_details(self) -> LoginPageData:

        validation = self.user_repository.validate_signup_data(request.form["User Name"],
                                                               request.form["Password"],
                                                               request.form["Confirmed"],
                                                               request.form["First Name"],
                                                               request.form["Surname"])

        if validation.state == State.Warning:
            message = validation.message
        else:
            # Passwords need to be stored in database as hash digests to maintain security. Therefore, need to convert
            # the password provided by the user to bytes so that hashlib's sha256 method can get
            # its hash digest (Python, 2024a; W3 Schools, 2024).
            bytes_password = hashlib.sha256(request.form["Password"].encode())

            # Use hexidigest to retrieve the hash digest of the password
            hash_digest = bytes_password.hexdigest()

            self.user_repository.add_user(request.form["User Name"],
                                          hash_digest,
                                          request.form["Account Type"],
                                          request.form["First Name"],
                                          request.form["Surname"],
                                          25 if request.form["Account Type"] == 'basic' else 0,
                                          None)

            message = "Your account has been set up, please log in."

        return LoginPageData(None,
                             validation.state,
                             message,
                             False)
