from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from controller.main_cliente import MainCliente
from model.conexion import Conexion


class LoginCliente(QMainWindow):
    def __init__(self):
        super(LoginCliente, self).__init__()
        loadUi("/home/juan/dev/reservapp/view/login_cliente.ui", self)
        self.bt_crear_cuenta.clicked.connect(self.cambiar_registro)
        self.bt_login.clicked.connect(self.login)

    def cambiar_registro(self):
        from controller.creacion_cuenta import CrearCliente

        self.registro = CrearCliente()
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
