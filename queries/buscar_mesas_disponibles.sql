WITH reserved_tables AS (
  SELECT mes_id
  FROM enc_reservas
  WHERE ere_fecha = %s
    AND (
      (%s BETWEEN ere_hora_inicio AND ere_hora_fin) OR
      (%s BETWEEN ere_hora_inicio AND ere_hora_fin) OR
      (ere_hora_inicio BETWEEN %s AND %s) OR
      (ere_hora_fin BETWEEN %s AND %s)
    )
)
SELECT mes_nro_mesa, mes_capacidad
FROM mesas
WHERE mes_estado = 'a'
  AND mes_id NOT IN (SELECT mes_id FROM reserved_tables);
