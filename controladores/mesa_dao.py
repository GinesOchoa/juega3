from flask import request, session, render_template
import json
from modelos.mesa import Mesa

class MesaDAO:
    def __init__(self, json_file):
        self.json_file = json_file

    # Método para generar un nuevo ID de reserva
    def generar_id_reserva(self):
        reservas = self.cargar_reservas()
        if not reservas:
            return 1
        else:
            return reservas[-1]['id'] + 1

    # Método para guardar una reserva en el archivo JSON
    def guardar_reserva(self, mesa):
        reserva_data = {
            "id": mesa.id_reserva,
            "usuario": mesa.usuario,
            "mesa": mesa.id_mesa,
            "fecha_reserva": mesa.fecha_reserva,
            "fecha_liberacion": mesa.fecha_liberacion,
            "hora_reserva": mesa.hora_reserva,
            "hora_liberacion": mesa.hora_liberacion
        }
        reservas = self.cargar_reservas()
        reservas.append(reserva_data)
        with open(self.json_file, "w") as archivo:
            json.dump(reservas, archivo, indent=4)

    # Método para cargar las reservas desde el archivo JSON
    def cargar_reservas(self):
        try:
            with open(self.json_file, "r") as archivo:
                reservas = json.load(archivo)
                return reservas
        except FileNotFoundError:
            return []

    # Método para obtener una reserva por su ID
    def obtener_reserva_por_id(self, reserva_id):
        reservas = self.cargar_reservas()
        for reserva in reservas:
            if reserva['id'] == reserva_id:
                return reserva
        return None

    # Método para reservar una mesa
    def reservar_mesa(self, id_mesa):
    
        mesa_id = request.form.get("mesa")
        fecha_reserva = request.form.get("fecha_reserva")
        fecha_liberacion = request.form.get("fecha_liberacion")
        hora_reserva = request.form.get("hora_reserva")
        hora_liberacion = request.form.get("hora_liberacion")
        usuario = session.get('usuario')
        reserva_id = self.generar_id_reserva()
    
        # Establecer la mesa como no disponible
        disponible = False
    
     # Crear la instancia de Mesa con todos los argumentos requeridos
        mesa = Mesa(mesa_id, reserva_id, usuario, disponible, fecha_reserva, fecha_liberacion, hora_reserva, hora_liberacion)
    
        # Guardar la reserva
        self.guardar_reserva(mesa) 
        
    
    # Método para obtener todas las mesas desde el archivo JSON
    def obtener_mesas(self):
        with open(self.json_file, 'r') as file:
            return json.load(file)

    
