class UserLoginData:
    def __init__(self,
                 user_id: int,
                 user_name: str,
                 password: str,
                 user_role: str,
                 password_attempts: int):
        self.user_id = user_id
        self.user_name = user_name
        self.password = password
        self.user_role = user_role
        self.password_attempts = password_attempts
