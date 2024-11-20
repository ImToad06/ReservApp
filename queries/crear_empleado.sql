INSERT INTO usuarios (
  usu_nombres, usu_apellidos,
  usu_cc, usu_fecha_nacimiento,
  ema_id, dir_id, tel_id, usu_tipo
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
