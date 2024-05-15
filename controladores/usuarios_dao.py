import json
import re  # Importar el módulo de expresiones regulares

class UsuariosDAO:
    def __init__(self, json_file):
        self.json_file = json_file

    # Método para obtener un usuario por sus credenciales (username y password)
    def obtener_usuario_por_credenciales(self, username, password):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
            usuarios = data['usuarios']  
            for user in usuarios:
                if user['username'] == username and user['password'] == password:
                    return user
        return None

    # Método para obtener un usuario por su nombre de usuario (username)
    def obtener_usuario_por_username(self, username):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
            usuarios = data['usuarios']  
            for user in usuarios:
                if user['username'] == username:
                    return user
        return None

    # Método para agregar un nuevo usuario a la base de datos
    def agregar_usuario(self, usuario):
        with open(self.json_file, 'r+') as file:
            data = json.load(file)
            usuarios = data['usuarios']
            usuarios.append(usuario)
            file.seek(0)
            json.dump(data, file, indent=4)  # Escribir los datos actualizados en el archivo JSON
            file.truncate()

    # Método para actualizar la información de un usuario existente
    def actualizar_usuario(self, usuario_actualizado):
        with open(self.json_file, 'r+') as file:
            data = json.load(file)
            usuarios = data['usuarios']
            for index, user in enumerate(usuarios):
                if user['id'] == usuario_actualizado['id']:
                    usuarios[index] = usuario_actualizado
                    file.seek(0)
                    json.dump(data, file, indent=4)  # Escribir los datos actualizados en el archivo JSON
                    file.truncate()
                    return True
        return False

    # Método para eliminar un usuario de la base de datos por su ID
    def eliminar_usuario(self, id_usuario):
        with open(self.json_file, 'r+') as file:
            data = json.load(file)
            usuarios = data['usuarios']
            for index, user in enumerate(usuarios):
                if user['id'] == id_usuario:
                    del usuarios[index]
                    file.seek(0)
                    json.dump(data, file, indent=4)  # Escribir los datos actualizados en el archivo JSON
                    file.truncate()
                    return True
        return False

    # Función para validar la contraseña
    def validar_contrasena(self, password):
        # Utilizamos una expresión regular para verificar la validez de la contraseña
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
