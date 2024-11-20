SELECT
  mes_id, mes_nro_mesa, mes_capacidad
FROM
  mesas m
WHERE
  m.mes_nro_mesa = %s and m.mes_estado = 'a';
