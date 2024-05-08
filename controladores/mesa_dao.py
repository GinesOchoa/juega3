from flask import request, session, flash
import json
from datetime import datetime
from modelos.mesa import Mesa

class MesaDAO:
    def __init__(self, mesa_file, eventos_file):
        self.mesa_file = mesa_file
        self.eventos_file = eventos_file


    def generar_id_reserva(self):
        reservas = self.cargar_reservas()
        if not reservas or not reservas["mesas"]:
            return 1
    
        max_id_reserva = max(reserva['id_reserva'] for mesa in reservas["mesas"] for reserva in mesa.get("reservas", []))
        return max_id_reserva + 1

    def generar_id_evento(self):
        eventos = self.cargar_eventos()
        return max(evento['id'] for evento in eventos) + 1 if eventos else 1

    def guardar_reserva(self, mesa):
        mesa_id = mesa.id_mesa
        fecha_reserva = request.form.get("fecha_reserva")
        fecha_liberacion = request.form.get("fecha_liberacion")
        hora_reserva = request.form.get("hora_reserva")
        hora_liberacion = request.form.get("hora_liberacion")
        usuario = session.get('usuario')
        reserva_id = self.generar_id_reserva()
        
        reservas = self.cargar_reservas()
        for m in reservas.get("mesas", []):
            if m["id"] == mesa_id and (not m['reservas'] or any(reserva["disponible"] for reserva in m['reservas'])):
                
                for reserva_existente in m["reservas"]:
                    if (reserva_existente["fecha_reserva"] == fecha_reserva and
                        reserva_existente["fecha_liberacion"] == fecha_liberacion and
                        reserva_existente["hora_reserva"] == hora_reserva and
                        reserva_existente["hora_liberacion"] == hora_liberacion):
                        print("La reserva ya existe para esta mesa.")
                        return
                
                reserva_data = {
                    "disponible": True,
                    "id_reserva": reserva_id,
                    "fecha_reserva": fecha_reserva,
                    "hora_reserva": hora_reserva,
                    "fecha_liberacion": fecha_liberacion,
                    "hora_liberacion": hora_liberacion,
                    "usuario": usuario
                }
                m["reservas"].append(reserva_data)
                self.guardar_en_archivo('mesa.json', reservas)
                self.actualizar_disponibilidad_mesas()
                flash('Reserva realizada con éxito', 'success')

                evento_id = self.generar_id_evento()
                evento_reserva = {
                    "id": evento_id,
                    "titulo": "Reserva",
                    "descripcion": f"Reserva de mesa {mesa_id} por {usuario}",
                    "fecha_reserva": fecha_reserva,
                    "hora_inicio": hora_reserva,
                    "fecha_liberacion": fecha_liberacion,
                    "hora_fin": hora_liberacion,
                    "color": "green" if mesa.disponible else "red"
                }
                eventos = self.cargar_eventos()
                eventos.append(evento_reserva)
                self.guardar_en_archivo('eventos.json', eventos)
                break
        else:
            print("La mesa no está disponible en este momento.")

    def cargar_desde_archivo(self, nombre_archivo):
        try:
            with open(nombre_archivo, "r") as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            return []

    def guardar_en_archivo(self, nombre_archivo, datos):
        with open(nombre_archivo, "w") as archivo:
            json.dump(datos, archivo, indent=4)

    def actualizar_disponibilidad_mesas(self):
        reservas = self.cargar_reservas()
        mesas = reservas.get('mesas', [])

        for mesa in mesas:
            for reserva in mesa['reservas']:
                fecha_inicio_reserva = datetime.strptime(reserva['fecha_reserva'] + ' ' + reserva['hora_reserva'], '%Y-%m-%d %H:%M')
                fecha_fin_reserva = datetime.strptime(reserva['fecha_liberacion'] + ' ' + reserva['hora_liberacion'], '%Y-%m-%d %H:%M')

                for otra_reserva in mesa['reservas']:
                    if reserva == otra_reserva:
                        continue

                    otra_fecha_inicio_reserva = datetime.strptime(otra_reserva['fecha_reserva'] + ' ' + otra_reserva['hora_reserva'], '%Y-%m-%d %H:%M')
                    otra_fecha_fin_reserva = datetime.strptime(otra_reserva['fecha_liberacion'] + ' ' + otra_reserva['hora_liberacion'], '%Y-%m-%d %H:%M')

                    if (fecha_inicio_reserva <= otra_fecha_fin_reserva and otra_fecha_inicio_reserva <= fecha_fin_reserva):
                        break

        self.guardar_en_archivo('mesa.json', reservas)

    def cargar_reservas(self):
        return self.cargar_desde_archivo('mesa.json')

    def cargar_eventos(self):
        return self.cargar_desde_archivo('eventos.json')

    def obtener_mesas(self):
        return self.cargar_reservas()

    def guardar_mesas(self, mesas):
        self.guardar_en_archivo("mesa.json", mesas)

    def guardar_eventos(self, eventos):
        self.guardar_en_archivo("eventos.json", eventos)

    def obtener_mesa_por_id(self, mesa_id):
        mesas = self.obtener_mesas()["mesas"]
        for mesa in mesas:
            if mesa["id"] == mesa_id:
                return Mesa(mesa["id"], [], False, None, None, None, None, None) 
        return None
