import psycopg2


class Conexion:
    def __init__(self) -> None:
        self.conexion = psycopg2.connect(user="juan", dbname="juan")
        self.cursor = self.conexion.cursor()
