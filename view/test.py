import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


class bienvenida(QMainWindow):
    def __init__(self):
        super(bienvenida, self).__init__()
        loadUi("/home/juan/dev/reservapp/view/bienvenida.ui", self)
        self.bt_cliente.clicked.connect(cambiar_vista)


class cliente_login(QMainWindow):
    def __init__(self):
        super(cliente_login, self).__init__()
        loadUi("usuarios-login.ui", self)


def cambiar_vista():
    inicio.hide()
    login.show()


aplicacion = QApplication(sys.argv)
inicio = bienvenida()
login = cliente_login()
inicio.show()
sys.exit(aplicacion.exec_())
