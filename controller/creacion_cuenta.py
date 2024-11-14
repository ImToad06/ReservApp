from datetime import date

from PyQt5.QtWidgets import QDialog, QMainWindow
from PyQt5.uic import loadUi

from controller.login_usuario import LoginCliente
from model.conexion import Conexion
from model.modelos import Usuario


class CrearCliente(QMainWindow):
    def __init__(self):
        super(CrearCliente, self).__init__()
        loadUi("/home/juan/dev/reservapp/view/registro_cliente.ui", self)
        self.bt_crear_cuenta.clicked.connect(self.crear_cuenta)

    def crear_cuenta(self):
        usuario = self.obtener_datos()
        if self.datos_completos(usuario):
            db = Conexion()
            if self.cuenta_existente(usuario.telefono, usuario.email):
                self.l_error.setText("Error! Correo o telefono ya en uso.")
                return
            consultas = self.obtener_consultas()

            db.cursor.execute(
                consultas[3], (usuario.telefono, date.today().strftime("%Y-%m-%d"))
            )
            db.cursor.execute(
                consultas[0], (usuario.direccion, date.today().strftime("%Y-%m-%d"))
            )
            db.cursor.execute(
                consultas[2], (usuario.email, date.today().strftime("%Y-%m-%d"))
            )
            db.conexion.commit()
            db.cursor.execute(consultas[5], (usuario.email,))
            ema_id = db.cursor.fetchone()
            db.cursor.execute(consultas[4], (usuario.telefono,))
            tel_id = db.cursor.fetchone()
            db.cursor.execute(consultas[6], (usuario.direccion,))
            dir_id = db.cursor.fetchone()
            db.cursor.execute(
                consultas[1],
                (
                    usuario.nombres,
                    usuario.apellidos,
                    usuario.cedula,
                    usuario.fnaci,
                    ema_id,
                    dir_id,
                    tel_id,
                    "c",
                    "a",
                    usuario.clave,
                ),
            )
            db.conexion.commit()
            db.conexion.close()
            self.login = LoginCliente()
            self.close()
            self.login.show()
            self.confirmacion = ConfirmacionCreacionCliente()
            self.confirmacion.show()
        else:
            self.l_error.setText("Error! datos incompletos.")

    def obtener_datos(self) -> Usuario:
        usuario = Usuario()
        usuario.nombres = self.le_nombre.text().lower()
        usuario.apellidos = self.le_apellido.text().lower()
        usuario.cedula = self.le_dni.text()
        fnaci = self.de_fnaci.date()
        usuario.fnaci = fnaci.toString("dd-MM-yyyy")
        usuario.email = self.le_email.text().lower()
        usuario.direccion = self.le_direccion.text().lower()
        usuario.telefono = self.le_telefono.text()
        usuario.clave = self.le_clave.text()
        return usuario

    def cuenta_existente(self, telefono, email) -> bool:
        db = Conexion()
        consultas = self.obtener_consultas()
        db.cursor.execute(consultas[6], (email,))
        ema_id = db.cursor.fetchone()
        db.cursor.execute(consultas[4], (telefono,))
        tel_id = db.cursor.fetchone()
        if ema_id is not None or tel_id is not None:
            return True
        else:
            return False

    def obtener_consultas(self):
        with open("/home/juan/dev/reservapp/queries/crear_direccion.sql", "r") as query:
            crear_direccion = query.read()
        with open("/home/juan/dev/reservapp/queries/crear_telefono.sql", "r") as query:
            crear_telefono = query.read()
        with open("/home/juan/dev/reservapp/queries/crear_email.sql", "r") as query:
            crear_email = query.read()
        with open("/home/juan/dev/reservapp/queries/crear_cliente.sql", "r") as query:
            crear_cliente = query.read()
        with open("/home/juan/dev/reservapp/queries/buscar_telefono.sql", "r") as query:
            buscar_telefono = query.read()
        with open(
            "/home/juan/dev/reservapp/queries/buscar_direccion.sql", "r"
        ) as query:
            buscar_direccion = query.read()
        with open("/home/juan/dev/reservapp/queries/buscar_email.sql", "r") as query:
            buscar_email = query.read()
        return (
            crear_direccion,
            crear_cliente,
            crear_email,
            crear_telefono,
            buscar_telefono,
            buscar_direccion,
            buscar_email,
        )

    def datos_completos(self, usuario: Usuario) -> bool:
        if len(usuario.nombres) == 0:
            return False
        elif len(usuario.apellidos) == 0:
            return False
        elif len(usuario.cedula) == 0:
            return False
        elif len(usuario.fnaci) == 0:
            return False
        elif len(usuario.email) == 0:
            return False
        elif len(usuario.direccion) == 0:
            return False
        elif len(usuario.telefono) == 0:
            return False
        elif len(usuario.clave) == 0:
            return False
        else:
            return True


class ConfirmacionCreacionCliente(QDialog):
    def __init__(self):
        super(ConfirmacionCreacionCliente, self).__init__()
        loadUi("/home/juan/dev/reservapp/view/confirmacion_creacion_cliente.ui", self)
        self.bt_ok.clicked.connect(lambda: self.close())
