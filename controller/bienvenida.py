from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from controller.login_usuario import LoginCliente, LoginEmpleado


class Bienvenida(QMainWindow):
    def __init__(self):
        super(Bienvenida, self).__init__()
        loadUi("/home/juan/dev/reservapp/view/bienvenida.ui", self)
        self.login_cliente = LoginCliente()
        self.login_empleado = LoginEmpleado()
        self.B_cliente.clicked.connect(self.cambiar_login_cliente)
        self.B_empleado.clicked.connect(self.cambiar_login_empleado)

    def cambiar_login_cliente(self):
        self.close()
        self.login_cliente.show()

    def cambiar_login_empleado(self):
        self.close()
        self.login_empleado.show()
