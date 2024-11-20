UPDATE usuarios
SET
  usu_nombres = %s, usu_apellidos = %s,
  usu_cc = %s, usu_fecha_nacimiento = TO_DATE(%s, 'YYYY-MM-DD'),
  ema_id = %s, dir_id = %s, tel_id = %s,
  usu_clave = %s
WHERE
  usu_id = %s;
