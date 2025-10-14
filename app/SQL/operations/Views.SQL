--VISTA PARA EL LLENADO DE LA DIMENSION DE CONVENIOS 
CREATE OR REPLACE VIEW operations."v_d_convenios" AS
SELECT DISTINCT 
    tipo,
    (fecha_inicializacion - fecha_inicio) AS Vigencia,
    estado
FROM operations."convenio";

DELETE FROM datawarehouse."D_CONVENIOS";

SELECT setval(
    pg_get_serial_sequence('datawarehouse."D_CONVENIOS"', 'llaveconvenios'),
    1,
    false
);

INSERT INTO datawarehouse."D_CONVENIOS"(tipo, vigencia, estado)
SELECT tipo, vigencia, estado
FROM operations."v_d_convenios";

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


