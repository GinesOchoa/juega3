import json
import re

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
            usuarios.append(usuario)
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def actualizar_usuario(self, usuario_actualizado):
        with open(self.json_file, 'r+') as file:
            data = json.load(file)
            usuarios = data['usuarios']
            for index, user in enumerate(usuarios):
                if user['id'] == usuario_actualizado['id']:
                    usuarios[index] = usuario_actualizado
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

        # Función para validar la contraseña
    def validar_contrasena(self, password):
        # Al menos 8 caracteres, una letra mayúscula, una minúscula, un número y un carácter especial
        patron = r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+}{:;\'?/>.<,])(?=.*[^\s]).{8,}'
        return re.match(patron, password)

    # Función para validar el correo electrónico
    def validar_correo(self, email):
        # Utilizamos una expresión regular para verificar el formato del correo electrónico
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email)

    # Función para validar el formato del teléfono
    def validar_telefono(self, telefono):
        # Utilizamos una expresión regular para verificar el formato del teléfono
        patron = r'^[0-9]{9}$'
        return re.match(patron, telefono)

    # Función para validar el formato del código postal
    def validar_codigo_postal(self, codigo_postal):
        # Utilizamos una expresión regular para verificar el formato del código postal
        patron = r'^[0-9]{5}$'
        return re.match(patron, codigo_postal)