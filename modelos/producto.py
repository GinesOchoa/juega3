class Producto:
    def __init__(self, idProducto, nombre, descripcion):
        self.idProducto = idProducto
        self.nombre = nombre
        self.descripcion = descripcion

class JuegoCompra(Producto):
    def __init__(self, idProducto, nombre, precio, descripcion, stock):
        super().__init__(idProducto, nombre, descripcion)
        self.precio = precio
        self.stock = stock

class JuegoAlquiler(Producto):
    def __init__(self, idProducto, nombre, precio_por_hora, descripcion, disponible_para_alquilar):
        super().__init__(idProducto, nombre, descripcion)
        self.precio_por_hora = precio_por_hora
        self.disponible_para_alquilar = disponible_para_alquilar
        self.fecha_alquiler = None
        self.fecha_devolucion = None
        self.hora_alquiler = None
        self.hora_devolucion = None

