import json

class AdminDAO:
    def __init__(self, json_file):
        self.json_file = json_file

    def verificarCredenciales(self, username, password):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
            for admin in data:
                if admin['username'] == username and admin['password'] == password:
                    return True
        return False