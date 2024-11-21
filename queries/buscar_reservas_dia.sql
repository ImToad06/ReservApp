SELECT
  m.mes_nro_mesa, u.usu_nombres,
  e.ere_nro_personas, e.ere_hora_inicio
FROM
  enc_reservas e INNER JOIN mesas m ON e.mes_id = m.mes_id
  INNER JOIN usuarios u ON e.usu_id = u.usu_id
WHERE
  e.ere_fecha = %s;
