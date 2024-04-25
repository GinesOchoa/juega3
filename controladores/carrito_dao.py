from operator import index

from items import data

carrito = []

class CarritoDao:

    def mensaje_carrito():
        if len(carrito) == 0:
            return "El carrito está vacío"
        else:
            return "Aquí está su carrito"


    def agregar_al_carrito(producto):
        for obj in data:
            if obj["idProducto"] == int(producto):
                carrito.append((len(carrito), obj))


    def eliminar_del_carrito(producto):
        for i, obj in enumerate(carrito):
            if i == int(producto):
                carrito.remove(obj)


    def eliminar_todo_carrito():
        carrito.clear()


    def calcular_total():
        total = 0.00
        for obj in carrito:
        total = total + obj[1]['precio']
        return total


    def nueva_lista(antigua_lista, nueva_lista):
        for each in antigua_lista:
            nueva_lista.append(each)


    def aplicar_descuento(total, descuento):
        total_antiguo = total
        if descuento == "ahorra20":
            total = total_antiguo * 0.8
        elif descuento == "mitad_precio":
            total = total_antiguo * 0.5
        return total



