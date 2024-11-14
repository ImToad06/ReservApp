from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from controller.login_usuario import LoginCliente


class Bienvenida(QMainWindow):
    def __init__(self):
        super(Bienvenida, self).__init__()
        loadUi("/home/juan/dev/reservapp/view/welcome.ui", self)
        self.login_cliente = LoginCliente()
        self.B_cliente.clicked.connect(self.cambiar_login_usuario)

    def cambiar_login_usuario(self):
        self.hide()
        self.login_cliente.show()
