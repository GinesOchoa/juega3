class Mesa:
    def __init__(self, id_mesa, disponible=True, fecha_reserva=None, fecha_liberacion=None):
        self.id_mesa = id_mesa
        self.disponible = disponible
        self.fecha_reserva = None
        self.fecha_liberacion = None