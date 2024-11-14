import sys

from PyQt5.QtWidgets import QApplication

from controller.bienvenida import Bienvenida
from model.conexion import Conexion


def main():
    app = QApplication(sys.argv)
    db = Conexion()
    bienvenida = Bienvenida()
    bienvenida.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
