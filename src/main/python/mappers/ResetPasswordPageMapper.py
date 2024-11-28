from flask import request
from common.enums.State import State
from domains.user.UserRepositoryInterface import IUserRepository
from mappers.BaseMapper import BaseMapper
from blueprints.models.ResetPasswordPageData import ResetPasswordPageData
import hashlib

class ResetPasswordPageMapper(BaseMapper):
    def __init__(self, user_repository: IUserRepository,):
        self.user_repository = user_repository

    def map_initial_page_data(self):
        return ResetPasswordPageData(State.Normal, None)

    def map_reset_page_data(self, reset_id: str):

        # Does email match id?
        expected_email = self.user_repository.get_email_by_id(reset_id)
        actual_email = request.form["email address"]

        if expected_email != actual_email:
            state = State.Warning
            message = "Provided email address is incorrect."
        else:
            password = request.form["new password"]
            confirm_password = request.form["confirm password"]

            password_validation = self.user_repository.validation_password(password, confirm_password)

            if password_validation.state == State.Warning:
                state = password_validation.state
                message = password_validation.message
            else:
                # Passwords need to be stored in database as hash digests to maintain security. Therefore, need to convert
                # the password provided by the user to bytes so that hashlib's sha256 method can get
                # its hash digest (Python, 2024a; W3 Schools, 2024).
                bytes_password = hashlib.sha256(password.encode())

                # Use hexidigest to retrieve the hash digest of the password
                hash_digest = bytes_password.hexdigest()

                self.user_repository.update_password_by_reset_id(reset_id, hash_digest)
                self.user_repository.clear_expiry_data(reset_id)

                state = State.Success
                message = "Thank you, your password has been changed"

        return ResetPasswordPageData(state=state,
                                     message=message)

    def map_error(self):
        state = State.Error
        message = "Something has gone wrong, please refresh and try again"

        return ResetPasswordPageData(state=state,
                                     message=message)