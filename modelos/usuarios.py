class Usuario:
    def __init__(self, id, username, password, nombre, apellidos, email, telefono, admin=False):
        self.id = id
        self.username = username
        self.password = password
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.telefono = telefono 
        self.admin = admin

class ClienteFisico(Usuario):
    def __init__(self, id, username, password, nombre, apellidos, email, telefono):
        super().__init__(id, username, password, nombre, apellidos, email, telefono)
        self.tipo = "Fisico"

class ClienteOnline(Usuario):
    def __init__(self, id, username, password, nombre, apellidos, email, telefono, direccion_envio, provincia, localidad, nacionalidad, codigo_postal):
        super().__init__(id, username, password, nombre, apellidos, email, telefono)

        self.tipo = "Online"
        self.direccion_envio = direccion_envio
        self.provincia = provincia
        self.localidad = localidad
        self.nacionalidad = nacionalidad
        self.codigo_postal = codigo_postal

class Admin(Usuario):
    def __init__(self, id, username, password, nombre, apellidos, email, telefono):
        super().__init__(id, username, password, nombre, apellidos, email, telefono, admin=True)

class Premium(Usuario):
    def __init__(self, id, username, password, nombre, apellidos, email, telefono, gasto_mensual, beneficios):
        super().__init__(id, username, password, nombre, apellidos, email, telefono)

        self.gasto_mensual = gasto_mensual
        self.beneficios = beneficios

