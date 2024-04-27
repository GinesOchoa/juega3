from datetime import datetime

class Venta:
    def __init__(self, venta_id, usuario, productos, precio_total):
        self.venta_id = venta_id
        self.usuario = usuario
        self.productos = productos
        self.precio_total = precio_total
        self.fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
