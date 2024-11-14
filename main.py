import sys

from PyQt5.QtWidgets import QApplication

from controller.bienvenida import Bienvenida


def main():
    app = QApplication(sys.argv)
    bienvenida = Bienvenida()
    bienvenida.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
