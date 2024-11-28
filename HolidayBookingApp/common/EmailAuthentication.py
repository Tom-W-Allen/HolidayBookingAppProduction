class EmailAuthenticationDetails:
    def __init__(self, password, sender, server_url):
        self.password = password
        self.sender = sender
        self.server_url = server_url