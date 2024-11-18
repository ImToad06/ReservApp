from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from model.conexion import Conexion
from model.modelos import Usuario


class MainCliente(QMainWindow):
    def __init__(self, usu_id):
        super(MainCliente, self).__init__()
        loadUi("/home/juan/dev/reservapp/view/main_cliente.ui", self)
        self.usu_id = usu_id
        self.pg_mis_reservas.hide()
        self.pg_mi_cuenta.hide()
        self.pg_reservar.show()
        self.bt_reservar.clicked.connect(self.cambiar_reservar)
        self.bt_mis_reservas.clicked.connect(self.cambiar_mis_reservas)
        self.bt_mi_cuenta.clicked.connect(self.cambiar_mi_cuenta)
        self.usuario = obtener_usuario(self.usu_id)
        saludo = self.usuario.nombres.split()[0]
        self.l_bienvenida.setText(f"Bienvenido, {saludo}!")

    def cambiar_reservar(self):
        self.pg_mis_reservas.hide()
        self.pg_mi_cuenta.hide()
        self.pg_reservar.show()

    def cambiar_mis_reservas(self):
        self.pg_mi_cuenta.hide()
        self.pg_reservar.hide()
        self.pg_mis_reservas.show()

    def cambiar_mi_cuenta(self):
        self.pg_mis_reservas.hide()
        self.pg_reservar.hide()
        self.pg_mi_cuenta.show()


def obtener_usuario(usu_id):
    with open("/home/juan/dev/reservapp/queries/buscar_usuario.sql", "r") as query:
        buscar_usuario = query.read()
    bd = Conexion()
    bd.cursor.execute(buscar_usuario, (usu_id,))
    usuario_t = bd.cursor.fetchone()
    usuario = Usuario()
    if usuario_t is not None:
        usuario.nombres = usuario_t[1]
        usuario.apellidos = usuario_t[2]
        usuario.cedula = usuario_t[8]
        usuario.fnaci = usuario_t[9]
        usuario.email = usuario_t[3]
        usuario.direccion = usuario_t[4]
        usuario.telefono = usuario_t[5]
        usuario.clave = usuario_t[6]
    return usuario
