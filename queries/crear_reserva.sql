INSERT INTO enc_reservas (
  usu_id, ere_fecha, ere_nro_personas,
  ere_estado, mes_id, ere_hora_inicio,
  ere_hora_fin
) VALUES (
  %s, to_date(%s, 'YYYY-MM-DD'),
  %s, 'a', %s, %s, %s
);
