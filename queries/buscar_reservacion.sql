SELECT
  e.ere_id, e.ere_fecha, 
  e.ere_hora_inicio, e.ere_nro_personas
FROM
  enc_reservas e INNER JOIN usuarios u ON e.usu_id = u.usu_id
WHERE
  e.usu_id = %s and (e.ere_estado = 'a' or e.ere_estado = 'f');
