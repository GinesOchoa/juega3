import json
from datetime import datetime

class MesaDAO:
    def __init__(self, json_file):
        self.json_file = json_file

    def obtener_mesas(self):
        with open(self.json_file, 'r') as file:
            return json.load(file)

    def guardar_mesas(self, mesas):
        with open(self.json_file, 'w') as file:
            json.dump(mesas, file, indent=4)

    def reservar_mesa(self):
        if not self.disponible:
            print("La mesa no está disponible para reservar en este momento.")
            return
        self.fecha_reserva = datetime.now()
        self.disponible = False
        print("Mesa reservada con éxito.")

    def liberar_mesa(self):
        if self.disponible:
            print("La mesa ya está libre.")
            return
        self.fecha_liberacion = datetime.now()
        self.disponible = True
        print("Mesa liberada con éxito.")

    def calcular_tiempo_reservado(self):
        if not self.fecha_reserva or not self.fecha_liberacion:
            print("La mesa no ha sido reservada o liberada.")
            return
        tiempo_reservado = self.fecha_liberacion - self.fecha_reserva
        return tiempo_reservado