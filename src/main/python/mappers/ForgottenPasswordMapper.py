from flask import session, request
from blueprints.models.ForgottenPasswordPageData import ForgottenPasswordPageData
from common.enums.State import State
from domains.user.UserRepositoryInterface import IUserRepository
from mappers.BaseMapper import BaseMapper
from common.EmailFunctions import get_email_authentication_details, send_email
from common.Logging import write_log
import string
import random
import datetime

class ForgottenPasswordMapper(BaseMapper):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def map_initial_page_data(self) -> ForgottenPasswordPageData:

        return ForgottenPasswordPageData(State.Normal,
                                         None,
                                         False)

    def map_send_email(self) -> ForgottenPasswordPageData:

        state = State.Normal
        message = None
        successful_request = False

        if not self.user_repository.is_postgreSQL():
            state = State.Warning
            message = ("Application is being run locally. Emails cannot be sent as credentials are not stored in this environment."
                       "Please use the testing or production environment.")

        else:
            user_id = self.user_repository.get_user_id_from_email(request.form["Registered Password"])
            user_details = self.user_repository.get_public_user_details(user_id)
            if user_id is None:
                pass # Do not give indication whether an account exists
            else:
                url_identifier = None
                identifier_exists = False

                # Create a random identifier to build the reset url
                while url_identifier is None or identifier_exists:

                    url_identifier = ''.join(random.choices(string.ascii_letters, k=10))
                    identifier_exists = self.user_repository.reset_identifier_exists(url_identifier)

                self.user_repository.update_reset_identifier(url_identifier, int(user_id))

                authentication = get_email_authentication_details()

                email_message = ("You have received this email because a password reset was requested for your account, please use the link below: \n\n"
                                 f"{authentication.server_url}/reset?id={url_identifier}\n\n"
                                 f"If you did not request a reset, please ensure that your accounts are secure.")

                send_email(email_message, request.form["Registered Password"], "Holiday Booking Application Password Reset", authentication)

                expiry_date_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
                expiry_date = f"{expiry_date_time.year}-{expiry_date_time.month}-{expiry_date_time.day}"
                expiry_time = f"{expiry_date_time.hour}:{expiry_date_time.minute}:{expiry_date_time.second}"
                write_log(user_details.user_name, "Reset Email", f"Account with username: {user_details.user_name} requested a password reset email")
                self.user_repository.update_reset_expiry(expiry_date, expiry_time, int(user_id))

                successful_request = True

        return ForgottenPasswordPageData(state,
                                         message,
                                         successful_request)

    def map_error(self) -> ForgottenPasswordPageData:
        message = "Something went wrong and your request could not be processed. Please refresh and try again."
        session["refresh_page"] = "yes"
        return  ForgottenPasswordPageData(State.Error,
                                          message,
                                          False)