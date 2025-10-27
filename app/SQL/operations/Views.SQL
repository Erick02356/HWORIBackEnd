--VISTA PARA EL LLENADO DE LA DIMENSION DE CONVENIOS 

BEGIN;

MERGE INTO datawarehouse."D_CONVENIOS" AS d
USING (
  SELECT codigo, tipo, vigencia, estado
  FROM operations."v_d_convenios"
) AS s
ON (d.codigo = s.codigo)
WHEN MATCHED THEN
  UPDATE SET
    tipo     = s.tipo,
    vigencia = s.vigencia,
    estado   = s.estado
WHEN NOT MATCHED THEN
  INSERT (codigo, tipo, vigencia, estado)
  VALUES (s.codigo, s.tipo, s.vigencia, s.estado);

-- (Opcional) Marcar como Inactivo los que ya no vienen en la fuente
UPDATE datawarehouse."D_CONVENIOS" d
SET estado = 'Inactivo'
WHERE NOT EXISTS (
  SELECT 1 FROM operations."v_d_convenios" s WHERE s.codigo = d.codigo
) AND d.estado <> 'Inactivo';

COMMIT;
--VISTAS PARA EL LLENADO DEL HECHO PL/SQL

CREATE OR REPLACE VIEW operations.vw_convenios_reducida AS
SELECT
    c.codigo AS "CodigoConvenio",
    c.tipo AS "TipoConvenio",
    (c.fecha_inicializacion - c.fecha_inicio) AS "VigenciaConvenio",
    c.estado AS "EstadoConvenio"
FROM operations.convenio c;


CREATE OR REPLACE VIEW parameters.vw_stg_movilidades_enriquecida AS
SELECT
    s.*,
    c."TipoConvenio",
    c."VigenciaConvenio",
    c."EstadoConvenio"
FROM parameters."stg_movilidades" s
LEFT JOIN operations.vw_convenios_reducida c
    ON s."codigoconvenio" = c."CodigoConvenio";


