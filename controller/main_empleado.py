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

        self.bt_actualizar_reservas.clicked.connect(self.cambiar_reservas)
        self.bt_buscar_reserva.clicked.connect(self.buscar_reservas)
        self.bt_anadir_producto.clicked.connect(self.agregar_prod)
        self.bt_facturar_buscar.clicked.connect(self.mostrar_factura)
        self.bt_facturar_reserva.clicked.connect(self.facturar_reserva)
        db = Conexion()
        db.cursor.execute("SELECT ite_nombre FROM items WHERE ite_estado = 'a';")
        items = db.cursor.fetchall()
        db.conexion.close()
        for item in items:
            self.cb_anadir_producto.addItem(item[0])

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
        self.cb_anadir_producto.addItem(" ")

    def cambiar_facturar(self):
        self.pg_reservas.hide()
        self.pg_pedidos.hide()
        self.pg_facturar.show()

    def buscar_reservas(self):
        mes_nro_mesa = self.le_buscar_nro_mesa.text().strip()
        ere_hora = self.te_buscar_hora.time().toString("HH:mm:ss")
        reserva = buscar_reserva(mes_nro_mesa, ere_hora)
        if reserva is not None:
            self.l_info_buscar_reserva.setStyleSheet(
                "color: white; font: 14pt 'Noto Sans';"
            )
            self.l_info_buscar_reserva.setText(
                f"Reserva enconrada! su id es {reserva[0]}."
            )
            self.le_anadir_id_reserva.setText(f"{reserva[0]}")
        else:
            self.l_info_buscar_reserva.setStyleSheet(
                "color: red; font: 14pt 'Noto Sans';"
            )
            self.l_info_buscar_reserva.setText(f"Error: Reserva no encontrada.")

    def agregar_prod(self):
        ere_id = self.le_anadir_id_reserva.text().strip()
        ite_nom = self.cb_anadir_producto.currentText()
        with open("/home/juan/dev/reservapp/queries/buscar_item.sql", "r") as archivo:
            buscar_item = archivo.read()
        db = Conexion()
        db.cursor.execute(buscar_item, (ite_nom,))
        item = db.cursor.fetchone()
        cant = self.sb_cant_producto.value()
        if item is not None:
            db.cursor.execute(
                "INSERT INTO det_reservas VALUES(%s, %s, %s)", (ere_id, item[0], cant)
            )
        db.conexion.commit()
        db.conexion.close()
        self.l_info_insertar_prod.setStyleSheet("color: white; font: 14pt 'Noto Sans';")
        self.l_info_insertar_prod.setText(f"Producto añadido exitosamente.")
        self.cb_anadir_producto.setCurrentText(" ")
        self.sb_cant_producto.setValue(0)

    def mostrar_factura(self):
        mes_nro_mesa = self.le_facturar_nro_mesa.text().strip()
        ere_hora = self.te_facturar_hora.time().toString("HH:mm:ss")
        reserva = buscar_reserva(mes_nro_mesa, ere_hora)
        db = Conexion()
        with open(
            "/home/juan/dev/reservapp/queries/generar_factura.sql", "r"
        ) as archivo:
            generar_factura = archivo.read()
        if reserva is None:
            self.l_info_generar_factura.setText("Error: Reserva no encontrada.")
        else:
            db.cursor.execute(generar_factura, (reserva[0],))
            factura = db.cursor.fetchall()
            total = 0.0
            self.tw_items.setRowCount(0)

            for row_idx, item in enumerate(factura):
                self.tw_items.insertRow(row_idx)
                nombre, cantidad, precio, subtotal = item
                total += subtotal
                self.tw_items.setItem(row_idx, 0, QTableWidgetItem(str(nombre)))
                self.tw_items.setItem(row_idx, 1, QTableWidgetItem(str(cantidad)))
                self.tw_items.setItem(row_idx, 2, QTableWidgetItem(f"{precio:.2f}"))
                self.tw_items.setItem(row_idx, 3, QTableWidgetItem(f"{subtotal:.2f}"))
            self.l_total.setText(f"{total}")
        db.conexion.close()

    def facturar_reserva(self):
        db = Conexion()
        mes_nro_mesa = self.le_facturar_nro_mesa.text().strip()
        ere_hora = self.te_facturar_hora.time().toString("HH:mm:ss")
        reserva = buscar_reserva(mes_nro_mesa, ere_hora)
        if reserva is None:
            self.l_info_finalizar.setStyleSheet("color: red; font: 14pt 'Noto Sans';")
            self.l_info_finalizar.setText(f"Error: Reserva no encontrada;")
        else:
            with open(
                "/home/juan/dev/reservapp/queries/finalizar_reserva.sql", "r"
            ) as archivo:
                finalizar_reserva = archivo.read()
            db.cursor.execute(finalizar_reserva, (reserva[0],))
            db.conexion.commit()
            db.conexion.close()
            self.l_info_finalizar.setStyleSheet("color: white; font: 14pt 'Noto Sans';")
            self.l_info_finalizar.setText(
                f"Reserva facturada y finalizafa exitosamente."
            )


def obtener_reservas_dia():
    hoy = datetime.today().strftime("%Y-%m-%d")
    db = Conexion()
    with open(
        "/home/juan/dev/reservapp/queries/buscar_reservas_dia.sql", "r"
    ) as archivo:
        buscar_reservas_dia = archivo.read()
    db.cursor.execute(buscar_reservas_dia, (hoy,))
    reservas_dia = db.cursor.fetchall()
    db.conexion.close()
    return reservas_dia


def buscar_reserva(mes_nro_mesa, ere_hora):
    db = Conexion()
    hoy = datetime.today().strftime("%Y-%m-%d")
    with open("/home/juan/dev/reservapp/queries/buscar_reserva.sql", "r") as archivo:
        buscar_reserva = archivo.read()
    db.cursor.execute(
        buscar_reserva,
        (
            mes_nro_mesa,
            ere_hora,
            hoy,
        ),
    )
    reserva = db.cursor.fetchone()
    db.conexion.close()
    return reserva
