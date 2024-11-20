from datetime import date

from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from model.conexion import Conexion
from model.modelos import Item, Usuario


class MainAdmin(QMainWindow):
    def __init__(self, usu_id):
        super(MainAdmin, self).__init__()
        self.usu_id = usu_id
        from controller.obtener_objetos import obtener_usuario

        self.usuario = obtener_usuario(usu_id)
        loadUi("/home/juan/dev/reservapp/view/main_admin.ui", self)
        self.show()
        self.pg_cuentas.hide()
        self.pg_items.hide()
        self.pg_mesas.show()
        self.bt_mesas.clicked.connect(self.cambiar_mesas)
        self.bt_items.clicked.connect(self.cambiar_items)
        self.bt_cuentas.clicked.connect(self.cambiar_cuentas)
        saludo = self.usuario.nombres.split()[0]
        self.l_bienvenida.setText(f"Bienvenido, {saludo}!")
        self.bt_crear_mesa.clicked.connect(self.crear_mesa)
        self.bt_buscar_mesa.clicked.connect(self.buscar_mesa)
        self.bt_actualizar_mesa.clicked.connect(self.actualizar_mesa)
        self.bt_eliminar_mesa.clicked.connect(self.eliminar_mesa)
        self.bt_crear_item.clicked.connect(self.crear_item)
        self.bt_buscar_item.clicked.connect(self.buscar_item)
        self.bt_actualizar_item.clicked.connect(self.actualizar_item)
        self.bt_eliminar_item.clicked.connect(self.eliminar_item)
        self.bt_crear_cuenta.clicked.connect(self.crear_cuenta)

    def cambiar_mesas(self):
        self.pg_items.hide()
        self.pg_cuentas.hide()
        self.pg_mesas.show()

    def cambiar_items(self):
        self.pg_cuentas.hide()
        self.pg_mesas.hide()
        self.pg_items.show()

    def cambiar_cuentas(self):
        self.pg_items.hide()
        self.pg_mesas.hide()
        self.pg_cuentas.show()

    def crear_mesa(self):
        with open("/home/juan/dev/reservapp/queries/crear_mesa.sql", "r") as archivo:
            crear_mesa = archivo.read()
        db = Conexion()
        nro_mesa = self.le_crear_nro_mesa.text().strip()
        capacidad_mesa = self.le_crear_capacidad_mesa.text().strip()
        if mesa_existe(nro_mesa):
            self.l_info_crear_mesa.setStyleSheet("color: red;")
            self.l_info_crear_mesa.setText("Error! la mesa ya se encuentra creada.")
        else:
            db.cursor.execute(
                crear_mesa,
                (
                    nro_mesa,
                    capacidad_mesa,
                ),
            )
            db.conexion.commit()
            db.conexion.close()
            self.l_info_crear_mesa.setStyleSheet("color: white;")
            self.l_info_crear_mesa.setText("Mesa creada exitosamente.")
        db.conexion.close()

    def actualizar_mesa(self):
        db = Conexion()
        id_mesa = self.le_actualizar_id_mesa.text()
        mes_capacidad = self.le_actualizar_capacidad_mesa.text()
        with open(
            "/home/juan/dev/reservapp/queries/actualizar_mesa.sql", "r"
        ) as archivo:
            actualizar_mesa = archivo.read()
        db.cursor.execute("SELECT * FROM mesas WHERE mes_id = %s", (id_mesa,))
        mesa = db.cursor.fetchone()
        if mesa is not None:
            db.cursor.execute(
                actualizar_mesa,
                (
                    mes_capacidad,
                    id_mesa,
                ),
            )
            db.conexion.commit()
            self.l_info_actualizar_mesa.setStyleSheet("color: white;")
            self.l_info_actualizar_mesa.setText("Mesa actualizada exitosamente.")
        else:
            self.l_info_actualizar_mesa.setStyleSheet("color: red;")
            self.l_info_actualizar_mesa.setText("Error! La mesa no existe")
        db.conexion.close()

    def buscar_mesa(self):
        db = Conexion()
        nro_mesa = self.le_buscar_nro_mesa.text()
        with open("/home/juan/dev/reservapp/queries/buscar_mesa.sql", "r") as archivo:
            buscar_mesa = archivo.read()
        db.cursor.execute(buscar_mesa, (nro_mesa,))
        mesa = db.cursor.fetchone()
        if mesa is None:
            self.l_info_buscar_mesa.setStyleSheet("color: red;")
            self.l_info_buscar_mesa.setText("Error! la mesa no existe!")
        else:
            self.l_info_buscar_mesa.setStyleSheet("color: white;")
            self.l_info_buscar_mesa.setText(f"Mesa encontrada, su id es {mesa[0]}")
        db.conexion.close()

    def eliminar_mesa(self):
        db = Conexion()
        mes_id = self.le_eliminar_id_mesa.text()
        with open("/home/juan/dev/reservapp/queries/eliminar_mesa.sql", "r") as archivo:
            eliminar_mesa = archivo.read()
        db.cursor.execute("SELECT * FROM mesas WHERE mes_id = %s", (mes_id,))
        mesa = db.cursor.fetchone()
        if mesa is not None:
            db.cursor.execute(eliminar_mesa, (mes_id,))
            db.conexion.commit()
            self.l_info_eliminar_mesa.setStyleSheet("color: white;")
            self.l_info_eliminar_mesa.setText("Mesa eliminada exitosamente.")
        else:
            self.l_info_eliminar_mesa.setStyleSheet("color: red;")
            self.l_info_eliminar_mesa.setText("Error! La mesa no existe")
        db.conexion.close()

    def crear_item(self):
        db = Conexion()
        item = Item()
        item.nombre = self.le_crear_nombre_item.text().lower().strip()
        item.descripcion = self.le_crear_descripcion_item.text().lower().strip()
        item.precio = self.le_crear_precio_item.text().strip()
        item.tipo = self.cb_tipo_item.currentText()
        if item_existe(item.nombre):
            self.l_info_crear_item.setStyleSheet("color: red;")
            self.l_info_crear_item.setText("Error! Item ya existe")
        else:
            crear_precio(item.precio)
            precio = buscar_precio(item.precio)
            tipo = ""
            match item.tipo:
                case "Bebida":
                    tipo = "b"
                case "Plato":
                    tipo = "p"
            with open(
                "/home/juan/dev/reservapp/queries/crear_item.sql", "r"
            ) as archivo:
                crear_item = archivo.read()
            if precio is not None:
                db.cursor.execute(
                    crear_item, (item.nombre, item.descripcion, precio[0], tipo)
                )
            db.conexion.commit()
            self.l_info_crear_item.setStyleSheet("color: white;")
            self.l_info_crear_item.setText("Item creado exitosamente")
        db.conexion.close()

    def buscar_item(self):
        db = Conexion()
        nombre = self.le_buscar_nombre_item.text().lower().strip()
        with open("/home/juan/dev/reservapp/queries/buscar_item.sql", "r") as archivo:
            buscar_item = archivo.read()
        db.cursor.execute(buscar_item, (nombre,))
        item = db.cursor.fetchone()
        db.conexion.close()
        if item is None:
            self.l_info_buscar_item.setStyleSheet("color: red;")
            self.l_info_buscar_item.setText("Error! El item no existe")
        else:
            self.l_info_buscar_item.setStyleSheet("color: white;")
            self.l_info_buscar_item.setText(f"Item encontrado, su id es {item[0]}")

    def actualizar_item(self):
        db = Conexion()
        ite_id = self.le_actualizar_id_item.text().strip()
        ite_nom = self.le_actualizar_nombre_item.text().lower().strip()
        pre_precio = self.le_actualizar_precio_item.text().strip()
        db.cursor.execute("SELECT * FROM items WHERE ite_id = %s", (ite_id,))
        item = db.cursor.fetchone()
        if item is not None:
            with open(
                "/home/juan/dev/reservapp/queries/actualizar_item.sql", "r"
            ) as archivo:
                actualizar_item = archivo.read()
            crear_precio(pre_precio)
            precio = buscar_precio(pre_precio)
            if precio is not None:
                db.cursor.execute(actualizar_item, (ite_nom, precio[0], ite_id))
            db.conexion.commit()
            db.conexion.close()
            self.l_info_actualizar_item.setStyleSheet("color: white;")
            self.l_info_actualizar_item.setText("Item actualizado exitosamente.")
        else:
            self.l_info_actualizar_item.setStyleSheet("color: red;")
            self.l_info_actualizar_item.setText("Error: el item no existe")
        db.conexion.close()

    def eliminar_item(self):
        db = Conexion()
        ite_id = self.le_eliminar_id_item.text().strip()
        db.cursor.execute("SELECT * FROM items WHERE ite_id = %s", (ite_id,))
        item = db.cursor.fetchone()
        if item is not None:
            with open(
                "/home/juan/dev/reservapp/queries/eliminar_item.sql", "r"
            ) as archivo:
                eliminar_item = archivo.read()
            db.cursor.execute(eliminar_item, (ite_id,))
            db.conexion.commit()
            self.l_info_eliminar_item.setStyleSheet("color: white;")
            self.l_info_eliminar_item.setText("Item eliminado exitosamente.")
        else:
            self.l_info_eliminar_item.setStyleSheet("color: red;")
            self.l_info_eliminar_item.setText("Error: Item no existe.")

    def crear_cuenta(self):
        db = Conexion()
        usuario = Usuario()
        usuario.nombres = self.le_crear_nombre_cuenta.text().lower().strip()
        usuario.apellidos = self.le_crear_apellido_cuenta.text().lower().strip()
        usuario.cedula = self.le_crear_cedula_cuenta.text().strip()
        usuario.fnaci = self.de_crear_fnaci_cuenta.date().toString("yyyy-MM-dd")
        usuario.email = self.le_crear_email_cuenta.text().lower().strip()
        usuario.direccion = self.le_crear_direccion_cuenta.text().lower().strip()
        usuario.telefono = self.le_crear_telefono_cuenta.text().strip()
        tipo = ""
        match self.cb_crear_tipo_cuenta.currentText():
            case "Empleado":
                tipo = "e"
            case "Administrador":
                tipo = "a"
        if cuenta_existe(usuario.cedula):
            self.l_info_crear_cuenta.setStyleSheet("color: red;")
            self.l_info_crear_cuenta.setText("Error: La cuenta ya existe.")
        else:
            email = buscar_email(usuario.email)
            telefono = buscar_telefono(usuario.telefono)
            if email is not None or telefono is not None:
                self.l_info_crear_cuenta.setStyleSheet("color: red;")
                self.l_info_crear_cuenta.setText(
                    "Error: El email o el telefono ya está en uso"
                )
            else:
                crear_telefono(usuario.telefono)
                crear_email(usuario.email)
                crear_direccion(usuario.direccion)
                email = buscar_email(usuario.email)
                telefono = buscar_telefono(usuario.telefono)
                direccion = buscar_direccion(usuario.direccion)
                with open(
                    "/home/juan/dev/reservapp/queries/crear_empleado.sql", "r"
                ) as archivo:
                    crear_empleado = archivo.read()
                if email is not None and direccion is not None and telefono is not None:
                    db.cursor.execute(
                        crear_empleado,
                        (
                            usuario.nombres,
                            usuario.apellidos,
                            usuario.cedula,
                            usuario.fnaci,
                            email[0],
                            direccion[0],
                            telefono[0],
                            tipo,
                        ),
                    )
                    db.conexion.commit()
                    self.l_info_crear_cuenta.setStyleSheet("color: white;")
                    self.l_info_crear_cuenta.setText("Cuenta creada exitosamente.")


def mesa_existe(nro_mesa) -> bool:
    db = Conexion()
    with open("/home/juan/dev/reservapp/queries/buscar_mesa.sql", "r") as archivo:
        buscar_mesa = archivo.read()
    db.cursor.execute(buscar_mesa, (nro_mesa,))
    mesa = db.cursor.fetchone()
    db.conexion.close()
    if mesa is None:
        return False
    else:
        return True


def item_existe(ite_nom) -> bool:
    db = Conexion()
    with open("/home/juan/dev/reservapp/queries/buscar_item.sql", "r") as archivo:
        buscar_item = archivo.read()
    db.cursor.execute(buscar_item, (ite_nom,))
    item = db.cursor.fetchone()
    db.conexion.close()
    if item is None:
        return False
    else:
        return True


def crear_precio(pre_precio):
    db = Conexion()
    precio = buscar_precio(pre_precio)
    if precio is None:
        with open("/home/juan/dev/reservapp/queries/crear_precio.sql", "r") as archivo:
            crear_precio = archivo.read()
        db.cursor.execute(crear_precio, (pre_precio,))
        db.conexion.commit()
    db.conexion.close()


def buscar_precio(pre_precio):
    db = Conexion()
    with open("/home/juan/dev/reservapp/queries/buscar_precio.sql", "r") as archivo:
        buscar_precio = archivo.read()
    db.cursor.execute(buscar_precio, (pre_precio,))
    precio = db.cursor.fetchone()
    db.conexion.close()
    return precio


def cuenta_existe(usu_cc) -> bool:
    db = Conexion()
    with open("/home/juan/dev/reservapp/queries/buscar_cuenta_cc.sql", "r") as archivo:
        buscar_cuenta = archivo.read()
    db.cursor.execute(buscar_cuenta, (usu_cc,))
    cuenta = db.cursor.fetchone()
    db.conexion.close()
    if cuenta is None:
        return False
    else:
        return True


def buscar_email(ema_email):
    db = Conexion()
    with open("/home/juan/dev/reservapp/queries/buscar_email.sql", "r") as archivo:
        buscar_email = archivo.read()
    db.cursor.execute(buscar_email, (ema_email,))
    email = db.cursor.fetchone()
    db.conexion.close()
    return email


def buscar_telefono(tel_telefono):
    db = Conexion()
    with open("/home/juan/dev/reservapp/queries/buscar_telefono.sql", "r") as archivo:
        buscar_telefono = archivo.read()
    db.cursor.execute(buscar_telefono, (tel_telefono,))
    telefono = db.cursor.fetchone()
    db.conexion.close()
    return telefono


def buscar_direccion(dir_direccion):
    db = Conexion()
    with open("/home/juan/dev/reservapp/queries/buscar_direccion.sql", "r") as archivo:
        buscar_direccion = archivo.read()
    db.cursor.execute(buscar_direccion, (dir_direccion,))
    direccion = db.cursor.fetchone()
    db.conexion.close()
    return direccion


def crear_email(ema_email):
    db = Conexion()
    email = buscar_email(ema_email)
    if email is None:
        with open("/home/juan/dev/reservapp/queries/crear_email.sql", "r") as archivo:
            crear_email = archivo.read()
        db.cursor.execute(crear_email, (ema_email, date.today().strftime("%Y-%m-%d")))
        db.conexion.commit()
    db.conexion.close()


def crear_telefono(tel_telefono):
    db = Conexion()
    telefono = buscar_telefono(tel_telefono)
    if telefono is None:
        with open(
            "/home/juan/dev/reservapp/queries/crear_telefono.sql", "r"
        ) as archivo:
            crear_telefono = archivo.read()
        db.cursor.execute(
            crear_telefono, (tel_telefono, date.today().strftime("%Y-%m-%d"))
        )
        db.conexion.commit()
    db.conexion.close()


def crear_direccion(dir_direccion):
    db = Conexion()
    direccion = buscar_direccion(dir_direccion)
    if direccion is None:
        with open(
            "/home/juan/dev/reservapp/queries/crear_direccion.sql", "r"
        ) as archivo:
            crear_direccion = archivo.read()
        db.cursor.execute(
            crear_direccion, (dir_direccion, date.today().strftime("%Y-%m-%d"))
        )
        db.conexion.commit()
    db.conexion.close()
