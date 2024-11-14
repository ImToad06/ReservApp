from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi


class MainCliente(QMainWindow):
    def __init__(self):
        super(MainCliente, self).__init__()
        loadUi("/home/juan/dev/reservapp/view/main_cliente.ui", self)
