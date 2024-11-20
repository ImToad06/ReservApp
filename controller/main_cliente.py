from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi

from controller.main_admin import buscar_email
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
        self.bt_actualizar_mis_datos.clicked.connect(self.cambiar_actualizar)
        self.bt_buscar_reserva.clicked.connect(self.buscar_mesas_disponibles)
        self.bt_confirmar_reserva.clicked.connect(self.confirmar_reserva)
        from controller.obtener_objetos import obtener_usuario

        self.usuario = obtener_usuario(self.usu_id)
        saludo = self.usuario.nombres.split()[0]
        self.l_bienvenida.setText(f"Bienvenido, {saludo}!")

    def cambiar_reservar(self):
        self.pg_mis_reservas.hide()
        self.pg_actualizar.hide()
        self.pg_mi_cuenta.hide()
        self.pg_reservar.show()

    def cambiar_mis_reservas(self):
        self.pg_mi_cuenta.hide()
        self.pg_reservar.hide()
        self.pg_actualizar.hide()
        self.pg_mis_reservas.show()

    def cambiar_mi_cuenta(self):
        self.pg_mis_reservas.hide()
        self.pg_actualizar.hide()
        self.pg_reservar.hide()
        self.pg_mi_cuenta.show()

    def cambiar_actualizar(self):
        self.pg_mis_reservas.hide()
        self.pg_reservar.hide()
        self.pg_mi_cuenta.hide()
        self.pg_actualizar.show()

    def buscar_mesas_disponibles(self):
        db = Conexion()
        fecha = self.de_freserva.date().toString("yyyy-MM-dd")
        hora_inicio = self.te_hreserva.time().toString("HH:mm:ss")
        hora_fin = self.te_hreserva.time().addSecs(2 * 3600).toString("HH:mm:ss")
        with open(
            "/home/juan/dev/reservapp/queries/buscar_mesas_disponibles.sql", "r"
        ) as archivo:
            buscar_mesas_disponibles = archivo.read()
        db.cursor.execute(
            buscar_mesas_disponibles,
            (
                fecha,
                hora_inicio,
                hora_fin,
                hora_inicio,
                hora_fin,
                hora_inicio,
                hora_fin,
            ),
        )
        mesas_disponibles = db.cursor.fetchall()
        self.tw_mesas.setRowCount(0)

        self.tw_mesas.setRowCount(len(mesas_disponibles))

        for row_idx, row_data in enumerate(mesas_disponibles):
            nro_mesa, capacidad_mesa = row_data
            self.tw_mesas.setItem(row_idx, 0, QTableWidgetItem(str(nro_mesa)))
            self.tw_mesas.setItem(row_idx, 1, QTableWidgetItem(str(capacidad_mesa)))

    def confirmar_reserva(self):
        db = Conexion()
        fecha = self.de_freserva.date().toString("yyyy-MM-dd")
        hora_inicio = self.te_hreserva.time().toString("HH:mm:ss")
        hora_fin = self.te_hreserva.time().addSecs(2 * 3600).toString("HH:mm:ss")
        nro_mesa = self.le_nro_mesa.text().strip()
        personas = self.le_nro_personas.text().strip()
        with open(
            "/home/juan/dev/reservapp/queries/buscar_mesas_disponibles.sql", "r"
        ) as archivo:
            buscar_mesas_disponibles = archivo.read()
        db.cursor.execute(
            buscar_mesas_disponibles,
            (
                fecha,
                hora_inicio,
                hora_fin,
                hora_inicio,
                hora_fin,
                hora_inicio,
                hora_fin,
            ),
        )
        mesa = buscar_mesa(nro_mesa)
        mesas_disponibles = db.cursor.fetchall()
        if mesa is not None and mesas_disponibles is not None:
            if mesa[2] < int(personas):
                self.l_info_reservar.setStyleSheet("color: red;")
                self.l_info_reservar.setText(
                    "Error: La mesa no tiene la capacidad necesaria."
                )
            elif mesa_libre(mesa, mesas_disponibles):
                with open(
                    "/home/juan/dev/reservapp/queries/crear_reserva.sql", "r"
                ) as archivo:
                    crear_reserva = archivo.read()
                db.cursor.execute(
                    crear_reserva,
                    (self.usu_id, fecha, personas, mesa[0], hora_inicio, hora_fin),
                )
                db.conexion.commit()
                self.l_info_reservar.setStyleSheet("color: white;")
                self.l_info_reservar.setText("Reserva hecha exitosamente.")
            else:
                self.l_info_reservar.setStyleSheet("color: red;")
                self.l_info_reservar.setText(
                    "Error: La mesa no se encuentra disponible"
                )
        db.conexion.close()


def buscar_mesa(nro_mesa):
    db = Conexion()
    with open("/home/juan/dev/reservapp/queries/buscar_mesa.sql", "r") as archivo:
        buscar_mesas = archivo.read()
    db.cursor.execute(buscar_mesas, (nro_mesa,))
    mesa = db.cursor.fetchone()
    return mesa


def mesa_libre(mesa, mesas_disponibles):
    for p_mesa in mesas_disponibles:
        if mesa[1] == p_mesa[0]:
            return True
    return False
