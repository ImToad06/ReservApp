from datetime import datetime

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi

from controller.obtener_objetos import obtener_usuario
from model.conexion import Conexion


class MainEmpleado(QMainWindow):
    def __init__(self, usu_id):
        super(MainEmpleado, self).__init__()
        self.usu_id = usu_id
        self.usuario = obtener_usuario(usu_id)
        loadUi("/home/juan/dev/reservapp/view/main_empleado.ui", self)
        self.cambiar_reservas()

        self.bt_reservas.clicked.connect(self.cambiar_reservas)
        self.bt_pedidos.clicked.connect(self.cambiar_pedidos)
        self.bt_facturar.clicked.connect(self.cambiar_facturar)

    def cambiar_reservas(self):
        self.pg_pedidos.hide()
        self.pg_facturar.hide()
        self.pg_reservas.show()
        self.l_bienvenida.setText(f"Bienvenido, {self.usuario.nombres.split()[0]}!")
        reservas = obtener_reservas_dia()
        self.tw_reservas.setRowCount(0)
        for row_idx, reserva in enumerate(reservas):
            self.tw_reservas.insertRow(row_idx)
            nro_mesa, nombre, personas, hora = reserva
            self.tw_reservas.setItem(row_idx, 0, QTableWidgetItem(str(nro_mesa)))
            self.tw_reservas.setItem(row_idx, 1, QTableWidgetItem(str(nombre)))
            self.tw_reservas.setItem(row_idx, 2, QTableWidgetItem(str(personas)))
            self.tw_reservas.setItem(row_idx, 3, QTableWidgetItem(str(hora)))

    def cambiar_pedidos(self):
        self.pg_facturar.hide()
        self.pg_reservas.hide()
        self.pg_pedidos.show()

    def cambiar_facturar(self):
        self.pg_reservas.hide()
        self.pg_pedidos.hide()
        self.pg_facturar.show()


def obtener_reservas_dia():
    hoy = datetime.today().strftime("%Y-%m-%d")
    db = Conexion()
    with open(
        "/home/juan/dev/reservapp/queries/buscar_reservas_dia.sql", "r"
    ) as archivo:
        buscar_reservas_dia = archivo.read()
    db.cursor.execute(buscar_reservas_dia, (hoy,))
    reservas_dia = db.cursor.fetchall()
    return reservas_dia
