users = {}


class User:
    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password

    def get_name(self):
        return self.name

    def get_password(self):
        return self.password
