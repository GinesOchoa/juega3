import json

class LoginDAO:
    def __init__(self, json_file):
        self.json_file = json_file

    def verificarCredenciales(self, username, password):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
            for user in data:
                if user['username'] == username and user['password'] == password:
                    return user['admin'] 
        return False
