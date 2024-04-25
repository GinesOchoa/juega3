import json

class ProductoDAO:
    
    def __init__(self, json_file):
        self.json_file = json_file

    def agregarProducto(self, producto):
        with open(self.json_file, 'r+') as file:
            data = json.load(file)
            data.append(vars(producto))
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def eliminarProducto(self, idProducto):
        with open(self.json_file, 'r+') as file:
            data = json.load(file)
            data = [p for p in data if p['idProducto'] != idProducto]
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def actualizarProducto(self, producto_actualizado):
        with open(self.json_file, 'r+') as file:
            data = json.load(file)
            for i, producto in enumerate(data):
                if producto['idProducto'] == producto_actualizado.idProducto:
                    data[i] = vars(producto_actualizado)
                    break
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    
    def listarProductos(self):
        with open(self.json_file, 'r') as file:
            return json.load(file)
        