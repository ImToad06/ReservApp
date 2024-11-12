import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


class bienvenida(QMainWindow):
    def __init__(self):
        super(bienvenida, self).__init__()
        loadUi("bienvenida.ui", self)
        self.bt_cliente.clicked.connect(self.cambiar_vista)
        self.show()

    def cambiar_vista(self):
        usuario = usuario_login()
        usuario.show()
        self.hide()


class usuario_login(QMainWindow):
    def __init__(self):
        super(usuario_login, self).__init__()
        loadUi("usuarios-login.ui", self)
        self.show()


raiz = QApplication(sys.argv)
ventana = bienvenida()
ventana.show()
raiz.exec_()
