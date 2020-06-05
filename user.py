class User:
    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password
        self.dbname = name

    def get_name(self):
        return self.name

    def get_dbname(self):
        return self.dbname

    def get_password(self):
        return self.password
