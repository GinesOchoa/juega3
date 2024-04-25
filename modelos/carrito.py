import json

class Carrito:
    def __init__(self, nombre_cliente, id_producto, cantidad, precio, total_carrito=0, descuento=0):
        self.nombre_cliente = nombre_cliente
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio = precio
        self.total_carrito = total_carrito
        self.descuento = descuento