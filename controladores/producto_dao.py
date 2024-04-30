import json
from datetime import datetime

class ProductoDAO:
    
    def __init__(self, json_file):
        self.json_file = json_file

    def agregar_juego(self, juego):
        with open(self.json_file, 'r+') as file:
            data = json.load(file)
            data.append(vars(juego))
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def eliminar_juego(self, idProducto):
        with open(self.json_file, 'r+') as file:
            data = json.load(file)
            data = [p for p in data if p['idProducto'] != idProducto]
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def actualizar_juego(self, juego_actualizado):
        with open(self.json_file, 'r+') as file:
            data = json.load(file)
            for i, juego in enumerate(data):
                if juego['idProducto'] == juego_actualizado.idProducto:
                    data[i] = vars(juego_actualizado)
                    break
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def listar_juegos(self):
        with open(self.json_file, 'r') as file:
            return json.load(file)

    def alquilar(self):
        if not self.disponible_para_alquilar:
            print("El juego no está disponible para alquilar en este momento.")
            return
        self.fecha_alquiler = datetime.now()
        self.disponible_para_alquilar = False
        print("Juego alquilado con éxito.")

    def devolver(self):
        if self.disponible_para_alquilar:
            print("El juego ya ha sido devuelto.")
            return
        self.fecha_devolucion = datetime.now()
        self.disponible_para_alquilar = True
        print("Juego devuelto con éxito.")

    def calcular_tiempo_alquilado(self):
        if not self.fecha_alquiler or not self.fecha_devolucion:
            print("El juego no ha sido alquilado o devuelto.")
            return
        tiempo_alquilado = self.fecha_devolucion - self.fecha_alquiler
        return tiempo_alquilado