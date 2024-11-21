SELECT
  e.ere_id
FROM
  enc_reservas e INNER JOIN mesas m ON e.mes_id = m.mes_id
WHERE
  m.mes_nro_mesa = %s AND e.ere_hora_inicio = %s
  AND e.ere_fecha = %s;
