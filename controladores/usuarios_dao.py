import json

class UsuariosDAO:
    def __init__(self, json_file):
        self.json_file = json_file

    def obtener_usuario_por_credenciales(self, username, password):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
            usuarios = data['usuarios']  
            for user in usuarios:
                if user['username'] == username and user['password'] == password:
                    return user
        return None

    def obtener_usuario_por_username(self, username):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
            usuarios = data['usuarios']  
            for user in usuarios:
                if user['username'] == username:
                    return user
        return None

    def agregar_usuario(self, usuario):
        with open(self.json_file, 'r+') as file:
            data = json.load(file)
            usuarios = data['usuarios']
            usuarios.append(usuario.__dict__)
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def actualizar_usuario(self, usuario_actualizado):
        with open(self.json_file, 'r+') as file:
            data = json.load(file)
            usuarios = data['usuarios']
            for index, user in enumerate(usuarios):
                if user['id'] == usuario_actualizado['id']:
                    usuarios[index] = usuario_actualizado.__dict__
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
                    return True
        return False

    def eliminar_usuario(self, id_usuario):
        with open(self.json_file, 'r+') as file:
            data = json.load(file)
            usuarios = data['usuarios']
            for index, user in enumerate(usuarios):
                if user['id'] == id_usuario:
                    del usuarios[index]
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
                    return True
        return False
