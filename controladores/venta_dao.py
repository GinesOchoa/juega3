import json

class VentaDAO:
    def __init__(self, json_file):
        self.json_file = json_file
        
    def generar_id_venta(self):
        ventas = self.cargar_ventas()
        if not ventas:
            return 1
        else:
            return ventas[-1]['id'] + 1

    def guardar_venta(self, venta):
        venta_id = self.generar_id_venta()
        venta_data = {
            "id": venta_id,
            "usuario": venta.usuario,
            "productos": venta.productos,
            "precio_total": venta.precio_total,
            "fecha_hora": venta.fecha_hora
        }
        ventas = self.cargar_ventas()
        ventas.append(venta_data)
        with open("ventas.json", "w") as archivo:
            json.dump(ventas, archivo, indent=4)

    def cargar_ventas(self):
        try:
            with open("ventas.json", "r") as archivo:
                ventas = json.load(archivo)
                return ventas
        except FileNotFoundError:
            return []

    def obtener_venta_por_id(self, venta_id):
        ventas = self.cargar_ventas()
        for venta in ventas:
            if venta['id'] == venta_id:
                return venta
        return None

    def eliminar_venta(self, venta_id):
        ventas = self.cargar_ventas()
        ventas_actualizadas = [venta for venta in ventas if venta['id'] != venta_id]
        with open("ventas.json", "w") as archivo:
            json.dump(ventas_actualizadas, archivo, indent=4)

    def actualizar_venta(self, venta_id, nuevos_datos):
        ventas = self.cargar_ventas()
        for venta in ventas:
            if venta['id'] == venta_id:
                venta.update(nuevos_datos)
                break
        with open("ventas.json", "w") as archivo:
            json.dump(ventas, archivo, indent=4)
