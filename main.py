from model.conexion import Conexion
from model.modelos import *


def main():
    persona = Usuario()
    persona.nombres = "juan"
    persona.apellidos = "reyes"
    mesa = Mesa()
    mesa.nro = 1
    mesa.capacidad = 4
    item = Item()
    item.nombre = "carne asada"
    item.descripcion = "carne asada 150 gr con papas fritas"
    item.precio = 240.89
    item1 = Item()
    item1.nombre = "coca-cola"
    item1.descripcion = "coca-cola personal 250ml"
    item1.precio = 25.2
    reserva = Reserva()
    reserva.usuario = persona
    reserva.mesa = mesa
    reserva.items.append(item)
    reserva.items.append(item1)
    # print(reserva.usuario.nombres)
    # print(reserva.mesa.nro)
    # for i in reserva.items:
    #     print(i.nombre, i.precio)
    bd = Conexion()
    bd.cursor.execute(
        """SELECT
            u.usu_nombres nombres, u.usu_apellidos apellidos, e.ema_email email,
            d.dir_direccion direccion, t.tel_telefono telefono, u.usu_cc id
           FROM
            usuarios u INNER JOIN emails e on u.ema_id = e.ema_id
            INNER JOIN direcciones d on u.dir_id = d.dir_id
            INNER JOIN telefonos t on u.tel_id = t.tel_id;
"""
    )
    usuario = bd.cursor.fetchone()
    print(usuario)


if __name__ == "__main__":
    main()
