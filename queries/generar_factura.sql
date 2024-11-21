SELECT
  i.ite_nombre,
  d.det_cant_prodc,
  p.pre_precio,
  (d.det_cant_prodc * p.pre_precio) AS subtotal
FROM
  det_reservas d
  INNER JOIN items i ON d.ite_id = i.ite_id
  INNER JOIN precios p ON i.pre_id = p.pre_id
  INNER JOIN enc_reservas e ON d.ere_id = e.ere_id
WHERE
  e.ere_id = %s AND e.ere_estado = 'a';
