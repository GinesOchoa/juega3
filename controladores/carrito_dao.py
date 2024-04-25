import json

carrito = []

class CarritoDAO:

    def __init__(self, json_file):
        self.json_file = json_file

    def mensaje_carrito(self):
        if len(carrito) == 0:
            return "El carrito está vacío"
        else:
            return "Aquí está su carrito"

    def agregar_al_carrito(self, producto):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
            for obj in data:
                if obj["idProducto"] == int(producto):
                    carrito.append((len(carrito), obj))
                    print("Producto agregado al carrito:", obj)
                
    def eliminar_del_carrito(self, producto_index):
        for i, obj in enumerate(carrito):
            if i == int(producto_index):
                print("Producto eliminado del carrito:", carrito[i])
                carrito.pop(i)  # Usar pop para eliminar el elemento en lugar de remove
                break  # Salir del bucle después de eliminar el producto
        print("Carrito actual después de eliminar:", carrito)       

    def eliminar_todo_carrito(self):
        carrito.clear()

    def calcular_total(self):
        total = 0.00
        with open(self.json_file, 'r') as file:
            data = json.load(file)
            for obj in carrito:
                for item in data:
                    if item['idProducto'] == obj[1]['idProducto']:
                        total += item['precio']
        return total

    def nueva_lista(self, antigua_lista, nueva_lista):
        for each in antigua_lista:
            nueva_lista.append(each)

    def aplicar_descuento(self, total, descuento):
        total_antiguo = total
        if descuento == "ahorra20":
            total = total_antiguo * 0.8
        elif descuento == "mitad_precio":
            total = total_antiguo * 0.5
        return total
