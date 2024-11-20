from model.conexion import Conexion
from model.modelos import Usuario


def obtener_usuario(usu_id):
    with open("/home/juan/dev/reservapp/queries/buscar_usuario.sql", "r") as query:
        buscar_usuario = query.read()
    bd = Conexion()
    bd.cursor.execute(buscar_usuario, (usu_id,))
    usuario_t = bd.cursor.fetchone()
    usuario = Usuario()
    if usuario_t is not None:
        usuario.nombres = usuario_t[1]
        usuario.apellidos = usuario_t[2]
        usuario.cedula = usuario_t[8]
        usuario.fnaci = usuario_t[9]
        usuario.email = usuario_t[3]
        usuario.direccion = usuario_t[4]
        usuario.telefono = usuario_t[5]
        usuario.clave = usuario_t[6]
    return usuario
