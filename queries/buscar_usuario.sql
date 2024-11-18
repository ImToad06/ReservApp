SELECT
  u.usu_id, u.usu_nombres, u.usu_apellidos,
  e.ema_email, d.dir_direccion, t.tel_telefono,
  u.usu_clave, u.usu_tipo, u.usu_cc,
  u.usu_fecha_nacimiento
FROM
  usuarios u INNER JOIN emails e ON u.ema_id = e.ema_id
  INNER JOIN direcciones d ON u.dir_id = d.dir_id
  INNER JOIN telefonos t ON u.tel_id = t.tel_id
WHERE
  u.usu_estado = 'a' and u.usu_id = %s;
