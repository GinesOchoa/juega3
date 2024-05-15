# Definición de la clase base Usuario
class Usuario:
    def __init__(self, id, username, password, nombre, apellidos, email, telefono, admin=False):
        # Inicialización de los atributos comunes a todos los usuarios
        self.id = id
        self.username = username
        self.password = password
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.telefono = telefono 
        self.admin = admin  # Un parámetro opcional para indicar si el usuario es un administrador o no

# Definición de la clase derivada ClienteFisico
class ClienteFisico(Usuario):
    def __init__(self, id, username, password, nombre, apellidos, email, telefono):
        super().__init__(id, username, password, nombre, apellidos, email, telefono)
        self.tipo = "Fisico"  # Definir el tipo de cliente como "Fisico"

# Definición de la clase derivada ClienteOnline
class ClienteOnline(Usuario):
    def __init__(self, id, username, password, nombre, apellidos, email, telefono, direccion_envio, provincia, localidad, nacionalidad, codigo_postal):
        super().__init__(id, username, password, nombre, apellidos, email, telefono)
        # Inicialización de atributos específicos para clientes online
        self.tipo = "Online"
        self.direccion_envio = direccion_envio
        self.provincia = provincia
        self.localidad = localidad
        self.nacionalidad = nacionalidad
        self.codigo_postal = codigo_postal

# Definición de la clase derivada Admin
class Admin(Usuario):
    def __init__(self, id, username, password, nombre, apellidos, email, telefono):
        super().__init__(id, username, password, nombre, apellidos, email, telefono, admin=True)
        # Establecer el atributo admin como True para indicar que este usuario es un administrador

# Definición de la clase derivada Premium
class Premium(Usuario):
    def __init__(self, id, username, password, nombre, apellidos, email, telefono, gasto_mensual, beneficios):
        super().__init__(id, username, password, nombre, apellidos, email, telefono)
        # Inicialización de atributos específicos para usuarios premium
        self.gasto_mensual = gasto_mensual
        self.beneficios = beneficios
