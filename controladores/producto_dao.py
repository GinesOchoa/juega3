import json
from datetime import datetime
from modelos.producto import JuegoAlquiler
import os

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

    def calcular_precio_total(self, precio_por_hora, fecha_alquiler, hora_alquiler, fecha_devolucion, hora_devolucion):
        fecha_hora_alquiler = datetime.strptime(f"{fecha_alquiler} {hora_alquiler}", "%Y-%m-%d %H:%M")
        fecha_hora_devolucion = datetime.strptime(f"{fecha_devolucion} {hora_devolucion}", "%Y-%m-%d %H:%M")
        tiempo_transcurrido = fecha_hora_devolucion - fecha_hora_alquiler
        horas_alquiler = tiempo_transcurrido.total_seconds() / 3600
        precio_total = precio_por_hora * horas_alquiler
        return precio_total

    def juego_disponible(self, id_juego):
        juego = self.obtener_juego_por_id(id_juego)
        return juego.disponible_para_alquilar
    
    def obtener_juego_por_id(self, idProducto):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
            for juego in data:
                if juego['idProducto'] == idProducto:
                    juego_alquiler = JuegoAlquiler(
                        juego['idProducto'],
                        juego['nombre'],
                        juego['precio_por_hora'],
                        juego['descripcion'],
                        juego['disponible_para_alquilar']
                    )
                    return juego_alquiler
            return None

    def cargar_recibos_alquiler(self):
        if os.path.exists('recibo_alquiler.json') and os.path.getsize('recibo_alquiler.json') > 0:
            with open('recibo_alquiler.json', 'r') as file:
                return json.load(file)
        else:
            return []

    def guardar_recibo_alquiler(self, recibo):
        recibos_existente = self.cargar_recibos_alquiler()  
        recibos_existente.append(recibo)
        with open('recibo_alquiler.json', 'w') as file:
            json.dump(recibos_existente, file)

    def actualizar_disponibilidad_juegos(self):
        alquileres = self.listar_alquileres()

        for alquiler in alquileres:
            fecha_inicio_alquiler = datetime.strptime(alquiler['fecha_alquiler'] + ' ' + alquiler['hora_alquiler'], '%Y-%m-%d %H:%M')
            fecha_fin_alquiler = datetime.strptime(alquiler['fecha_devolucion'] + ' ' + alquiler['hora_devolucion'], '%Y-%m-%d %H:%M')

            otros_alquileres = [otro for otro in alquileres if otro != alquiler]

            for otro_alquiler in otros_alquileres:
                otra_fecha_inicio_alquiler = datetime.strptime(otro_alquiler['fecha_alquiler'] + ' ' + otro_alquiler['hora_alquiler'], '%Y-%m-%d %H:%M')
                otra_fecha_fin_alquiler = datetime.strptime(otro_alquiler['fecha_devolucion'] + ' ' + otro_alquiler['hora_devolucion'], '%Y-%m-%d %H:%M')

                if (fecha_inicio_alquiler <= otra_fecha_fin_alquiler and otra_fecha_inicio_alquiler <= fecha_fin_alquiler):
                    alquiler['disponible_para_alquilar'] = False
                    break
            else:
                alquiler['disponible_para_alquilar'] = True

        self.guardar_en_archivo('recibo_alquiler.json', alquileres)


    def guardar_en_archivo(self, nombre_archivo, datos):
        with open(nombre_archivo, "w") as archivo:
            json.dump(datos, archivo, indent=4)

    def listar_alquileres(self):
        try:
            with open('recibo_alquiler.json', 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data  
                elif isinstance(data, dict):
                    return data.get('alquileres', [])  
                else:
                    return []  
        except (json.JSONDecodeError, FileNotFoundError):
           
            return []

    def cargar_alquileres(self):
        with open('recibo_alquiler.json', 'r') as file:
            alquileres = json.load(file)
        return alquileres