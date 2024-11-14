# User class required by Flask-Login (2024).
class UserSession:
    def __init__(self, user_id):
        self._user_id = str(user_id)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self._user_id
