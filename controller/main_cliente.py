from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
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
        self.bt_actualizar_mis_datos.clicked.connect(self.cambiar_actualizar)
        self.bt_buscar_reserva.clicked.connect(self.buscar_mesas_disponibles)
        self.bt_confirmar_reserva.clicked.connect(self.confirmar_reserva)
        self.bt_actualizar_mis_reservas.clicked.connect(self.actualizar_mis_reservas)
        self.bt_cancelar_reserva.clicked.connect(self.cancelar_reserva)
        self.bt_actualizar_mis_datos.clicked.connect(self.cambiar_actualizar)
        self.bt_actualizar_datos.clicked.connect(self.actualizar_datos)
        self.bt_eliminar_mi_cuenta.clicked.connect(self.eliminar_cuenta)
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
        db = Conexion()
        with open(
            "/home/juan/dev/reservapp/queries/buscar_reservacion.sql", "r"
        ) as archivo:
            buscar_reservacion = archivo.read()
        db.cursor.execute(buscar_reservacion, (self.usu_id,))
        reservas = db.cursor.fetchall()
        self.tw_mis_reservas.setRowCount(0)
        self.tw_mis_reservas.setRowCount(len(reservas))
        for row_idx, row_data in enumerate(reservas):
            id_reserva, fecha, hora, personas = row_data
            id_item = QTableWidgetItem(str(id_reserva))
            fecha_item = QTableWidgetItem(str(fecha))
            hora_item = QTableWidgetItem(str(hora))
            personas_item = QTableWidgetItem(str(personas))
            self.tw_mis_reservas.setItem(row_idx, 0, id_item)
            self.tw_mis_reservas.setItem(row_idx, 1, fecha_item)
            self.tw_mis_reservas.setItem(row_idx, 2, hora_item)
            self.tw_mis_reservas.setItem(row_idx, 3, personas_item)
        db.conexion.close()

    def cambiar_mi_cuenta(self):
        self.pg_mis_reservas.hide()
        self.pg_actualizar.hide()
        self.pg_reservar.hide()
        self.pg_mi_cuenta.show()
        db = Conexion()
        cedula = self.usuario.cedula
        with open(
            "/home/juan/dev/reservapp/queries/buscar_cuenta_cc.sql", "r"
        ) as archivo:
            buscar_cuenta = archivo.read()
        db.cursor.execute(buscar_cuenta, (cedula,))
        cuenta = db.cursor.fetchone()
        if cuenta is not None:
            self.le_nombres.setText(cuenta[1])
            self.le_apellidos.setText(cuenta[2])
            self.le_cedula.setText(cuenta[8])
            fecha = QDate(cuenta[9])
            self.de_fecnac.setDate(fecha)
            self.le_email.setText(cuenta[3])
            self.le_direccion.setText(cuenta[4])
            self.le_telefono.setText(cuenta[5])

    def cambiar_actualizar(self):
        self.pg_mis_reservas.hide()
        self.pg_reservar.hide()
        self.pg_mi_cuenta.hide()
        self.pg_actualizar.show()
        db = Conexion()
        cedula = self.usuario.cedula
        with open(
            "/home/juan/dev/reservapp/queries/buscar_cuenta_cc.sql", "r"
        ) as archivo:
            buscar_cuenta = archivo.read()
        db.cursor.execute(buscar_cuenta, (cedula,))
        cuenta = db.cursor.fetchone()
        if cuenta is not None:
            self.le_actualizar_nombre.setText(cuenta[1])
            self.le_actualizar_apellido.setText(cuenta[2])
            self.le_actualizar_cedula.setText(cuenta[8])
            fecha = QDate(cuenta[9])
            self.de_actualizar_fnac.setDate(fecha)
            self.le_actualizar_email.setText(cuenta[3])
            self.le_actualizar_direccion.setText(cuenta[4])
            self.le_actualizar_telefono.setText(cuenta[5])
            self.le_actualizar_clave.setText(cuenta[10])

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

    def actualizar_mis_reservas(self):
        db = Conexion()
        with open(
            "/home/juan/dev/reservapp/queries/buscar_reservacion.sql", "r"
        ) as archivo:
            buscar_reservacion = archivo.read()
        db.cursor.execute(buscar_reservacion, (self.usu_id,))
        reservas = db.cursor.fetchall()
        self.tw_mis_reservas.setRowCount(0)
        self.tw_mis_reservas.setRowCount(len(reservas))
        for row_idx, row_data in enumerate(reservas):
            id_reserva, fecha, hora, personas = row_data
            id_item = QTableWidgetItem(str(id_reserva))
            fecha_item = QTableWidgetItem(str(fecha))
            hora_item = QTableWidgetItem(str(hora))
            personas_item = QTableWidgetItem(str(personas))
            self.tw_mis_reservas.setItem(row_idx, 0, id_item)
            self.tw_mis_reservas.setItem(row_idx, 1, fecha_item)
            self.tw_mis_reservas.setItem(row_idx, 2, hora_item)
            self.tw_mis_reservas.setItem(row_idx, 3, personas_item)
        db.conexion.close()

    def cancelar_reserva(self):
        ere_id = self.le_cancelar_id_reserva.text().strip()
        db = Conexion()
        with open(
            "/home/juan/dev/reservapp/queries/cancelar_reserva.sql", "r"
        ) as archivo:
            cancelar_reserva = archivo.read()
        db.cursor.execute("SELECT * FROM enc_reservas WHERE ere_id = %s", (ere_id,))
        reserva = db.cursor.fetchone()
        if reserva is not None:
            if reserva[1] == self.usu_id:
                db.cursor.execute(cancelar_reserva, (ere_id,))
                db.conexion.commit()
                self.l_info_cancelar_reserva.setStyleSheet("color: white;")
                self.l_info_cancelar_reserva.setText("Reserva cancelada exitosamente.")
            else:
                self.l_info_cancelar_reserva.setStyleSheet("color: red;")
                self.l_info_cancelar_reserva.setText("Error: Reserva no encontrada.")
        else:
            self.l_info_cancelar_reserva.setStyleSheet("color: red;")
            self.l_info_cancelar_reserva.setText("Error: Reserva no encontrada.")

    def actualizar_datos(self):
        db = Conexion()
        usuario = Usuario()
        usuario.nombres = self.le_actualizar_nombre.text().strip().lower()
        usuario.apellidos = self.le_actualizar_apellido.text().strip().lower()
        usuario.cedula = self.le_actualizar_cedula.text().strip()
        usuario.fnaci = self.de_actualizar_fnac.date().toString("yyyy-MM-dd")
        usuario.email = self.le_actualizar_email.text().strip()
        usuario.direccion = self.le_actualizar_direccion.text().strip().lower()
        usuario.telefono = self.le_actualizar_telefono.text().strip()
        usuario.clave = self.le_actualizar_clave.text().strip()
        db.cursor.execute("SELECT * FROM usuarios WHERE usu_cc = %s", (usuario.cedula,))
        usu_id = db.cursor.fetchone()
        from controller.main_admin import (
            buscar_direccion,
            buscar_email,
            buscar_telefono,
            crear_direccion,
            crear_email,
            crear_telefono,
        )

        crear_email(usuario.email)
        crear_telefono(usuario.telefono)
        crear_direccion(usuario.direccion)
        ema_id = buscar_email(usuario.email)
        dir_id = buscar_direccion(usuario.direccion)
        tel_id = buscar_telefono(usuario.telefono)
        with open(
            "/home/juan/dev/reservapp/queries/actualizar_cliente.sql", "r"
        ) as archivo:
            actualizar_cuenta = archivo.read()
        if (
            ema_id is not None
            and dir_id is not None
            and tel_id is not None
            and usu_id is not None
        ):
            db.cursor.execute(
                actualizar_cuenta,
                (
                    usuario.nombres,
                    usuario.apellidos,
                    usuario.cedula,
                    usuario.fnaci,
                    ema_id[0],
                    dir_id[0],
                    tel_id[0],
                    usuario.clave,
                    usu_id[0],
                ),
            )
            self.l_info_actualizar_datos.setStyleSheet("color: white;")
            self.l_info_actualizar_datos.setText("Cuenta actualizada exitosamente.")
        db.conexion.commit()
        db.conexion.close()

    def eliminar_cuenta(self):
        confirm_dialog = QMessageBox(self)
        confirm_dialog.setIcon(QMessageBox.Warning)
        confirm_dialog.setWindowTitle("Confirmación")
        confirm_dialog.setText("¿Estás seguro que deseas eliminar tu cuenta?")
        confirm_dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        confirm_dialog.setDefaultButton(QMessageBox.Cancel)
        response = confirm_dialog.exec_()
        if response == QMessageBox.Ok:
            db = Conexion()
            usu_id = self.usu_id
            db.cursor.execute("SELECT * FROM usuarios WHERE usu_id = %s", (usu_id,))
            usuario = db.cursor.fetchone()
            if usuario is not None:
                with open(
                    "/home/juan/dev/reservapp/queries/eliminar_cuenta.sql", "r"
                ) as archivo:
                    eliminar_cuenta = archivo.read()
                db.cursor.execute(eliminar_cuenta, (usu_id,))
                db.conexion.commit()
                db.conexion.close()
            despedida = QMessageBox(self)
            despedida.setIcon(QMessageBox.Information)
            despedida.setWindowTitle("Cuenta Eliminada")
            despedida.setText("Su cuenta ha sido eliminada exitosamente.")
            despedida.setStandardButtons(QMessageBox.Ok)
            despedida.setDefaultButton(QMessageBox.Ok)
            despedida.exec_()
            from controller.bienvenida import Bienvenida

            self.bienvenida = Bienvenida()
            self.bienvenida.show()
            self.close()
        else:
            pass


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
