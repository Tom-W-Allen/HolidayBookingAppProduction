from typing import Optional


class PublicUser:
    def __init__(self,
                 user_id: int,
                 user_name: Optional[str],
                 account_type: str,
                 first_name: Optional[str],
                 surname: Optional[str],
                 manager: Optional[int],
                 email: Optional[str]):
        self.user_id = user_id
        self.user_name = user_name
        self.account_type = account_type
        self.first_name = first_name
        self.surname = surname
        self.manager = manager
        self.email = email

    def __eq__(self, other):
        return (self.user_id == other.user_id and
                self.user_name == other.user_name and
                self.first_name == other.first_name and
                self.surname == other.surname and
                self.account_type == other.account_type and
                self.manager == other.manager and
                self.email == other.email)
