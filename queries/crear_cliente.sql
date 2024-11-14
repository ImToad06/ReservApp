INSERT INTO usuarios (usu_nombres, usu_apellidos, usu_cc, usu_fecha_nacimiento,
ema_id, dir_id, tel_id, usu_tipo, usu_estado, usu_clave)
VALUES (%s, %s, %s, TO_DATE(%s, 'DD-MM-YYYY'), %s, %s, %s, %s, %s, %s);

