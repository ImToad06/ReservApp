from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class LoginCliente(QMainWindow):
    def __init__(self):
        super(LoginCliente, self).__init__()
        loadUi("/home/juan/dev/reservapp/view/login.ui", self)
