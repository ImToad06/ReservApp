from datetime import datetime


class Usuario:
    def __init__(self) -> None:
        self.nombres = ""
        self.apellidos = ""
        self.cedula = ""
        self.fnaci = ""
        self.email = ""
        self.direccion = ""
        self.telefono = ""
        self.clave = ""


class Mesa:
    def __init__(self) -> None:
        self.nro = 0
        self.capacidad = 0


class Item:
    def __init__(self) -> None:
        self.nombre = ""
        self.descripcion = ""
        self.precio = 0.0


class Reserva:
    def __init__(self) -> None:
        self.usuario = Usuario()
        self.mesa = Mesa()
        self.fecha = datetime.now()
        self.nro_personas = 0
        self.items = []
