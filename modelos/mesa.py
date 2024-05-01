class Mesa:
    def __init__(self, id_mesa, id_reserva, usuario, disponible, fecha_reserva, fecha_liberacion, hora_reserva, hora_liberacion):
        self.id_mesa = id_mesa
        self.id_reserva = id_reserva
        self.disponible = disponible
        self.usuario = usuario
        self.fecha_reserva = fecha_reserva
        self.fecha_liberacion = fecha_liberacion
        self.hora_reserva = hora_reserva
        self.hora_liberacion = hora_liberacion