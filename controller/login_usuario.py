from datetime import date

from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from controller.main_cliente import MainCliente
from model.conexion import Conexion
from model.modelos import Usuario


class LoginCliente(QMainWindow):
    def __init__(self):
        super(LoginCliente, self).__init__()
        loadUi("/home/juan/dev/reservapp/view/login_cliente.ui", self)
        self.registro = CrearCliente()
        self.bt_crear_cuenta.clicked.connect(self.cambiar_registro)
        self.bt_login.clicked.connect(self.login)

    def cambiar_registro(self):
        self.close()
        self.registro.show()

    def login(self):
        db = Conexion()
        email = self.le_email.text()
        clave = self.le_clave.text()
        db.cursor.execute(
            f"select e.ema_email, u.usu_clave from usuarios u inner join emails e on u.ema_id = e.ema_id where e.ema_email = '{email}'"
        )
        cuenta = db.cursor.fetchone()
        if cuenta is None:
            self.l_error.setText("Error! La cuenta no existe.")
        elif cuenta[1] != clave:
            self.l_error.setText("Error! Contraseña incorrecta.")
        elif cuenta[1] == clave:
            self.main_cliente = MainCliente()
            self.close()
            self.main_cliente.show()
        db.conexion.close()


class CrearCliente(QMainWindow):
    def __init__(self):
        super(CrearCliente, self).__init__()
        loadUi("/home/juan/dev/reservapp/view/registro_cliente.ui", self)
        self.bt_crear_cuenta.clicked.connect(self.crear_cuenta)

    def crear_cuenta(self):
        usuario = Usuario()
        usuario.nombres = self.le_nombre.text()
        usuario.apellidos = self.le_apellido.text()
        usuario.cedula = self.le_dni.text()
        fnaci = self.de_fnaci.date()
        usuario.fnaci = fnaci.toString("dd-MM-yyyy")
        usuario.email = self.le_email.text()
        usuario.direccion = self.le_direccion.text()
        usuario.telefono = self.le_telefono.text()
        usuario.clave = self.le_clave.text()
        if self.datos_completos(usuario):
            db = Conexion()
            with open(
                "/home/juan/dev/reservapp/queries/crear_direccion.sql", "r"
            ) as query:
                q_direccion = query.read()
            with open(
                "/home/juan/dev/reservapp/queries/crear_telefono.sql", "r"
            ) as query:
                q_telefono = query.read()
            with open("/home/juan/dev/reservapp/queries/crear_email.sql", "r") as query:
                q_email = query.read()
            with open(
                "/home/juan/dev/reservapp/queries/crear_cliente.sql", "r"
            ) as query:
                q_cliente = query.read()
            with open(
                "/home/juan/dev/reservapp/queries/buscar_telefono.sql", "r"
            ) as query:
                qb_telefono = query.read()
            with open(
                "/home/juan/dev/reservapp/queries/buscar_direccion.sql", "r"
            ) as query:
                qb_direccion = query.read()
            with open(
                "/home/juan/dev/reservapp/queries/buscar_email.sql", "r"
            ) as query:
                qb_email = query.read()
            db.cursor.execute(
                q_telefono, (usuario.telefono, date.today().strftime("%Y-%m-%d"))
            )
            db.cursor.execute(
                q_direccion, (usuario.direccion, date.today().strftime("%Y-%m-%d"))
            )
            db.cursor.execute(
                q_email, (usuario.email, date.today().strftime("%Y-%m-%d"))
            )
            db.conexion.commit()
            db.cursor.execute(
                f"SELECT emails.ema_id FROM emails where ema_email = '{usuario.email}'"
            )
            ema_id = db.cursor.fetchone()
            db.cursor.execute(
                f"SELECT telefonos.tel_id FROM telefonos where tel_telefono = '{usuario.telefono}'"
            )
            tel_id = db.cursor.fetchone()
            db.cursor.execute(
                f"SELECT direcciones.dir_id FROM direcciones where dir_direccion = '{usuario.direccion}'"
            )
            dir_id = db.cursor.fetchone()
            # db.cursor.execute(qb_email, (usuario.email))
            # ema_id = db.cursor.fetchone()
            # db.cursor.execute(qb_telefono, (usuario.telefono))
            # tel_id = db.cursor.fetchone()
            db.cursor.execute(
                q_cliente,
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
        else:
            self.l_error.setText("Error! datos incompletos.")

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


class LoginEmpleado(QMainWindow):
    def __init__(self):
        super(LoginEmpleado, self).__init__()
        loadUi("/home/juan/dev/reservapp/view/login_empleado.ui", self)
        self.bt_login.clicked.connect(self.login)

    def login(self):
        usu_cedula = self.le_dni.text()
        db = Conexion()
        db.cursor.execute(
            f"select u.usu_tipo from usuarios u where u.usu_cc = '{usu_cedula}'"
        )
        cuenta = db.cursor.fetchone()
        if cuenta is None:
            self.l_error.setText("Error! La cuenta no existe.")
        elif cuenta[0] == "c":
            self.l_error.setText("Error! La cuenta no es de tipo empleado.")
        else:
            self.main = MainCliente()
            self.close()
            self.main.show()
        db.conexion.close()
