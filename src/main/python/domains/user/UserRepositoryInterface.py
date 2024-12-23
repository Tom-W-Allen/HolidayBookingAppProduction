from domains.user.models.PublicUser import PublicUser
from domains.user.models.UserLoginData import UserLoginData
from domains.user.models.EditProfileValidation import EditProfileValidation
from domains.user.models.SignupValidation import SignupValidation
from domains.user.models.PasswordValidation import PasswordValidation
from common.enums.UserType import UserType
from persistence.Database import Database
from typing import Optional
import datetime


# For details on informal Python interfaces, see (Murphy, 2024).
class IUserRepository:
    def __init__(self, database: Database):
        self._database = database

    def is_postgreSQL(self):
        pass

    def reset_identifier_exists(self, identifier: str) -> bool:
        pass

    def get_user_id_from_email(self, email_address: str) -> int:
        pass

    def update_reset_identifier(self, identifier: str, user_id: int):
        pass

    def update_reset_expiry(self, expiry_day: str, expiry_time: str, user_id: int):
        pass

    def get_expiry_time(self, reset_id: str) -> Optional[datetime]:
        pass

    def update_password_by_reset_id(self, reset_id: str, password: str, salt: str):
        pass

    def validate_email(self, email: str) -> SignupValidation:
        pass

    def get_email_by_id(self, reset_id: str) -> str:
        pass

    def clear_expiry_data(self, reset_id: str):
        pass

    def add_user(self, username: str, password: str, account_type: str, first_name: str,
                 surname: str, holidays: int, manager: Optional[int], email: Optional[str]):
        pass

    def get_user_manager(self, user_id: int) -> int:
        pass

    def get_all_users(self) -> "list[PublicUser]":
        pass

    def get_public_user_details(self, user_id: int) -> PublicUser:
        pass

    def get_user_type_details(self, user_type: UserType):
        pass

    def get_user_login_details(self, user_name: str) -> Optional[UserLoginData]:
        pass

    def check_username_exists(self, user_name: int) -> bool:
        pass

    def update_user(self, user: PublicUser, password_updated: bool = False):
        pass

    def delete_user(self, user: PublicUser):
        pass

    def validate_edit_profile(self, proposed_details: PublicUser, password: str, confirmed_password: str) \
            -> EditProfileValidation:
        pass

    def validate_signup_data(self, username: str, password: str, confirmed_password: str,
                             first_name: str, surname: str) -> SignupValidation:
        pass

    def validation_password(self, password: str, confirmed_password: str) -> PasswordValidation:
        pass

    def store_proposed_password(self, user_id: int, password: str) -> None:
        pass

    def clear_password_change(self, user_id: int) -> None:
        pass

    def verify_password_change(self, user_id: int) -> bool:
        pass

    def get_password_attempts(self, user_id: int) -> int:
        pass

    def update_password_attempts(self, user_id: int, new_attempts: int) -> None:
        pass

    def approve_user(self, user_id: int) -> None:
        pass

    def get_admin_approved(self, user_id: int) -> str:
        pass

    def get_user_id_by_reset_id(self, reset_id: str) -> int:
        pass