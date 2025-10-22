🔹 MATERIALIZED VIEWS (base de dashboard)

-- =========================
-- 1 MVs: Movilidades por tiempo
-- =========================
DROP MATERIALIZED VIEW IF EXISTS datawarehouse.mv_movilidades_por_pais;

CREATE MATERIALIZED VIEW datawarehouse.mv_movilidades_por_pais AS
SELECT 
  l.paisorigen,
  l.paisdestino,
  COUNT(*)::bigint AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_LUGAR" l ON h.llavelugar = l.llavelugar
GROUP BY l.paisorigen, l.paisdestino;

CREATE UNIQUE INDEX IF NOT EXISTS ix_mv_movilidades_por_pais
  ON datawarehouse.mv_movilidades_por_pais (paisorigen, paisdestino);


-- =========================
-- 2 MVs: Movilidades por programa
-- =========================
DROP MATERIALIZED VIEW IF EXISTS datawarehouse.mv_movilidades_por_programa;

CREATE MATERIALIZED VIEW datawarehouse.mv_movilidades_por_programa AS
SELECT 
  p.nombreprograma,
  p.facultad,
  COUNT(*)::bigint AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_PROGRAMA" p ON h.llaveprograma = p.llaveprograma
GROUP BY p.nombreprograma, p.facultad;

CREATE UNIQUE INDEX IF NOT EXISTS ix_mv_movilidades_por_programa
  ON datawarehouse.mv_movilidades_por_programa (nombreprograma, facultad);


-- =========================
-- 3 MVs: Movilidades por convenio
-- =========================
DROP MATERIALIZED VIEW IF EXISTS datawarehouse.mv_movilidades_por_convenio;

CREATE MATERIALIZED VIEW datawarehouse.mv_movilidades_por_convenio AS
SELECT 
  c.tipo,
  c.vigencia,
  c.estado,
  COUNT(*)::bigint AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_CONVENIOS" c ON h.llaveconvenios = c.llaveconvenios
GROUP BY c.tipo, c.vigencia, c.estado;

CREATE UNIQUE INDEX IF NOT EXISTS ix_mv_movilidades_por_convenio
  ON datawarehouse.mv_movilidades_por_convenio (tipo, vigencia, estado);


-- =========================
-- 4 MVs: Movilidades por institución
-- =========================
DROP MATERIALIZED VIEW IF EXISTS datawarehouse.mv_movilidades_por_institucion;

CREATE MATERIALIZED VIEW datawarehouse.mv_movilidades_por_institucion AS
SELECT 
  l.institucionorigen,
  l.instituciondestino,
  COUNT(*)::bigint AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_LUGAR" l ON h.llavelugar = l.llavelugar
GROUP BY l.institucionorigen, l.instituciondestino;

CREATE UNIQUE INDEX IF NOT EXISTS ix_mv_movilidades_por_institucion
  ON datawarehouse.mv_movilidades_por_institucion (institucionorigen, instituciondestino);


-- =========================
-- 5 MVs: Movilidades por género
-- =========================
DROP MATERIALIZED VIEW IF EXISTS datawarehouse.mv_movilidades_por_genero;

CREATE MATERIALIZED VIEW datawarehouse.mv_movilidades_por_genero AS
SELECT 
  m.genero,
  COUNT(*)::bigint AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_MOVILIZANTE" m ON h.llavemovilizante = m.llavemovilizante
GROUP BY m.genero;

CREATE UNIQUE INDEX IF NOT EXISTS ix_mv_movilidades_por_genero
  ON datawarehouse.mv_movilidades_por_genero (genero);


-- =========================
-- 6 MVs: Movilidades por direccion (Entrante/Saliente)
-- =========================
DROP MATERIALIZED VIEW IF EXISTS datawarehouse.mv_movilidades_por_direccion;

CREATE MATERIALIZED VIEW datawarehouse.mv_movilidades_por_direccion AS
SELECT 
  mo.direccion,
  COUNT(*)::bigint AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_MOVILIDAD" mo ON h.llavemovilidad = mo.llavemovilidad
GROUP BY mo.direccion;

CREATE UNIQUE INDEX IF NOT EXISTS ix_mv_movilidades_por_direccion
  ON datawarehouse.mv_movilidades_por_direccion (direccion);


-- =========================
-- 7 MVs: Movilidades por tipo
-- =========================
DROP MATERIALIZED VIEW IF EXISTS datawarehouse.mv_movilidades_por_tipo;

CREATE MATERIALIZED VIEW datawarehouse.mv_movilidades_por_tipo AS
SELECT 
  mo.tipo,
  COUNT(*)::bigint AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_MOVILIDAD" mo ON h.llavemovilidad = mo.llavemovilidad
GROUP BY mo.tipo;

CREATE UNIQUE INDEX IF NOT EXISTS ix_mv_movilidades_por_tipo
  ON datawarehouse.mv_movilidades_por_tipo (tipo);


-- =========================
-- 8 MVs: Movilidades por modalidad
-- =========================
DROP MATERIALIZED VIEW IF EXISTS datawarehouse.mv_movilidades_por_modalidad;

CREATE MATERIALIZED VIEW datawarehouse.mv_movilidades_por_modalidad AS
SELECT 
  mo.modalidad,
  COUNT(*)::bigint AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_MOVILIDAD" mo ON h.llavemovilidad = mo.llavemovilidad
GROUP BY mo.modalidad;

CREATE UNIQUE_INDEX IF NOT EXISTS ix_mv_movilidades_por_modalidad
  ON datawarehouse.mv_movilidades_por_modalidad (modalidad);


🔹 VIEWS (derivadas de MVs para “TOP/Bottom”)
--1 Semestre con mayor número de movilidades
CREATE OR REPLACE VIEW datawarehouse.vw_semestre_top AS
SELECT "año", semestre, total_movilidades
FROM datawarehouse.mv_movilidades_por_tiempo
ORDER BY total_movilidades DESC
LIMIT 1;

--2 TOP 10 países con mayor cantidad de movilidades
CREATE OR REPLACE VIEW datawarehouse.vw_paises_top10 AS
SELECT paisorigen, paisdestino, total_movilidades
FROM datawarehouse.mv_movilidades_por_pais
ORDER BY total_movilidades DESC
LIMIT 10;

--3 BOTTOM 10 países con menor cantidad de movilidades (>0)
CREATE OR REPLACE VIEW datawarehouse.vw_paises_bottom10 AS
SELECT paisorigen, paisdestino, total_movilidades
FROM datawarehouse.mv_movilidades_por_pais
WHERE total_movilidades > 0
ORDER BY total_movilidades ASC
LIMIT 10;

--4 Programa con mayor número de movilidades
CREATE OR REPLACE VIEW datawarehouse.vw_programa_top AS
SELECT nombreprograma, total_movilidades
FROM datawarehouse.mv_movilidades_por_programa
ORDER BY total_movilidades DESC
LIMIT 1;

--5 Programa con menor número de movilidades
CREATE OR REPLACE VIEW datawarehouse.vw_programa_bottom AS
SELECT nombreprograma, total_movilidades
FROM datawarehouse.mv_movilidades_por_programa
ORDER BY total_movilidades ASC
LIMIT 1;

--6 Tipo de movilidad más realizada
CREATE OR REPLACE VIEW datawarehouse.vw_tipo_top AS
SELECT tipo, total_movilidades
FROM datawarehouse.mv_movilidades_por_tipo
ORDER BY total_movilidades DESC
LIMIT 1;

--7 Convenio con mayor número de movilidades
CREATE OR REPLACE VIEW datawarehouse.vw_convenio_top AS
SELECT tipo, vigencia, estado, total_movilidades
FROM datawarehouse.mv_movilidades_por_convenio
ORDER BY total_movilidades DESC
LIMIT 1;


🔹 FUNCIONES (parámetros de periodo / umbral)

-- 1) Total de movilidades en un periodo
CREATE OR REPLACE FUNCTION datawarehouse.fn_total_movilidades_periodo(anio INT, semestre INT)
RETURNS bigint
LANGUAGE sql
AS $$
SELECT COUNT(*)::bigint
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_TIEMPO" t ON h.llavetiempo = t.llavetiempo
WHERE t."año" = anio AND t.semestre = semestre;
$$;


-- 2) Movilidades ENTRANTES en un periodo
CREATE OR REPLACE FUNCTION datawarehouse.fn_movilidades_entrantes_periodo(anio INT, semestre INT)
RETURNS bigint
LANGUAGE sql
AS $$
SELECT COUNT(*)::bigint
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_TIEMPO" t ON h.llavetiempo = t.llavetiempo
JOIN datawarehouse."D_MOVILIDAD" m ON h.llavemovilidad = m.llavemovilidad
WHERE t."año" = anio AND t.semestre = semestre
  AND m.direccion = 'Entrante';
$$;


-- 3) Movilidades SALIENTES en un periodo
CREATE OR REPLACE FUNCTION datawarehouse.fn_movilidades_salientes_periodo(anio INT, semestre INT)
RETURNS bigint
LANGUAGE sql
AS $$
SELECT COUNT(*)::bigint
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_TIEMPO" t ON h.llavetiempo = t.llavetiempo
JOIN datawarehouse."D_MOVILIDAD" m ON h.llavemovilidad = m.llavemovilidad
WHERE t."año" = anio AND t.semestre = semestre
  AND m.direccion = 'Saliente';
$$;


-- 4) País que más movilidades realiza hacia la universidad en un periodo
CREATE OR REPLACE FUNCTION datawarehouse.fn_top_pais_origen_periodo(anio INT, semestre INT)
RETURNS TABLE (paisorigen text, total_movilidades bigint)
LANGUAGE sql
AS $$
SELECT l.paisorigen, COUNT(*)::bigint AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_LUGAR" l ON h.llavelugar = l.llavelugar
JOIN datawarehouse."D_TIEMPO" t ON h.llavetiempo = t.llavetiempo
WHERE t."año" = anio AND t.semestre = semestre
GROUP BY l.paisorigen
ORDER BY total_movilidades DESC
LIMIT 1;
$$;