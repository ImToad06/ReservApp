from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from controller.main_admin import MainAdmin
from controller.main_cliente import MainCliente
from controller.main_empleado import MainEmpleado
from model.conexion import Conexion


class LoginCliente(QMainWindow):
    def __init__(self):
        super(LoginCliente, self).__init__()
        loadUi("/home/juan/dev/reservapp/view/login_cliente.ui", self)
        self.bt_crear_cuenta.clicked.connect(self.cambiar_registro)
        self.bt_login.clicked.connect(self.login)
        self.bt_atras.clicked.connect(self.cambiar_atras)

    def cambiar_registro(self):
        from controller.creacion_cuenta import CrearCliente

        self.registro = CrearCliente()
        self.close()
        self.registro.show()

    def cambiar_atras(self):
        from controller.bienvenida import Bienvenida

        self.bienvenida = Bienvenida()
        self.close()
        self.bienvenida.show()

    def login(self):
        db = Conexion()
        email = self.le_email.text()
        clave = self.le_clave.text()
        db.cursor.execute(
            f"select u.usu_id, e.ema_email, u.usu_clave from usuarios u inner join emails e on u.ema_id = e.ema_id where e.ema_email = '{email}' and u.usu_estado = 'a';"
        )
        cuenta = db.cursor.fetchone()
        if cuenta is None:
            self.l_error.setText("Error! La cuenta no existe.")
        elif cuenta[2] != clave:
            self.l_error.setText("Error! Contraseña incorrecta.")
        elif cuenta[2] == clave:
            self.main_cliente = MainCliente(usu_id=cuenta[0])
            self.close()
            self.main_cliente.show()
        db.conexion.close()


class LoginEmpleado(QMainWindow):
    def __init__(self):
        super(LoginEmpleado, self).__init__()
        loadUi("/home/juan/dev/reservapp/view/login_empleado.ui", self)
        self.bt_login.clicked.connect(self.login)
        self.bt_atras.clicked.connect(self.cambiar_atras)

    def login(self):
        usu_cedula = self.le_dni.text()
        db = Conexion()
        db.cursor.execute(
            f"select u.usu_tipo, u.usu_id from usuarios u where u.usu_cc = '{usu_cedula}'"
        )
        cuenta = db.cursor.fetchone()
        if cuenta is None:
            self.l_error.setText("Error! La cuenta no existe.")
        elif cuenta[0] == "c":
            self.l_error.setText("Error! La cuenta no es de tipo empleado.")
        elif cuenta[0] == "e":
            self.main = MainEmpleado(cuenta[1])
            self.close()
            self.main.show()
        elif cuenta[0] == "a":
            self.main = MainAdmin(cuenta[1])
            self.close()
            self.main.show()
        db.conexion.close()

    def cambiar_atras(self):
        from controller.bienvenida import Bienvenida

        self.bienvenida = Bienvenida()
        self.close()
        self.bienvenida.show()
