--CONSULTAS OLAP

--1. Movilidades Totales
SELECT 
    t.año,
    t.semestre,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_TIEMPO" t ON h.llavetiempo = t.llavetiempo
GROUP BY t.año, t.semestre
ORDER BY t.año, t.semestre;


--2. Movilidades por País
SELECT 
    l.paisorigen,
    l.paisdestino,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_LUGAR" l ON h.llavelugar = l.llavelugar
GROUP BY l.paisorigen, l.paisdestino
ORDER BY total_movilidades DESC;

-- 3. Movilidades por Programa

SELECT 
    p.nombreprograma,
    p.facultad,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas"  h
JOIN datawarehouse."D_PROGRAMA" p ON h.llaveprograma = p.llaveprograma
GROUP BY p.nombreprograma, p.facultad
ORDER BY total_movilidades DESC;

-- 4. Movilidades por Convenio

SELECT 
    c.tipo,
    c.vigencia,
    c.estado,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas"  h
JOIN datawarehouse."D_CONVENIOS" c ON h.llaveconvenios = c.llaveconvenios
GROUP BY c.tipo, c.vigencia, c.estado
ORDER BY total_movilidades DESC;

-- 5. Movilidades por Institución

SELECT 
    l.institucionorigen,
    l.instituciondestino,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas"  h
JOIN datawarehouse."D_LUGAR" l ON h.llavelugar = l.llavelugar
GROUP BY l.institucionorigen, l.instituciondestino
ORDER BY total_movilidades DESC;

-- 6. Movilidades por Género 
SELECT 
    m.genero,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas"  h
JOIN datawarehouse."D_MOVILIZANTE" m ON h.llavemovilizante = m.llavemovilizante
GROUP BY m.genero
ORDER BY m.genero;

-- Edad

SELECT 
    m.edad,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas"  h
JOIN datawarehouse."D_MOVILIZANTE" m ON h.llavemovilizante = m.llavemovilizante
GROUP BY m.edad
ORDER BY m.edad;

--7. Movilidades por Dirección
SELECT 
    mo.direccion,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas"  h
JOIN datawarehouse."D_MOVILIDAD" mo ON h.llavemovilidad = mo.llavemovilidad
GROUP BY mo.direccion
ORDER BY total_movilidades DESC;

--8. Movilidades por Tipo
SELECT 
    mo.tipo,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas"  h
JOIN datawarehouse."D_MOVILIDAD" mo ON h.llavemovilidad = mo.llavemovilidad
GROUP BY mo.tipo
ORDER BY total_movilidades DESC;

-- 8.5 Movilidades por Modalidad
SELECT 
    mo.modalidad,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas"  h
JOIN datawarehouse."D_MOVILIDAD" mo ON h.llavemovilidad = mo.llavemovilidad
GROUP BY  mo.modalidad
ORDER BY total_movilidades DESC;

-- PREGUNTAS
-- 1. Número total de movilidades en un periodo de tiempo
SELECT 
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_TIEMPO" t ON h.llavetiempo = t.llavetiempo
WHERE t.año = 2025 AND t.semestre = 1;  -- ajusta periodo

-- 2. Movilidades entrantes en un periodo 
SELECT 
    COUNT(*) AS movilidades_entrantes
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_TIEMPO" t ON h.llavetiempo = t.llavetiempo
JOIN datawarehouse."D_MOVILIDAD" m ON h.llavemovilidad = m.llavemovilidad
WHERE t.año = 2024 AND t.semestre = 2
  AND m.direccion = 'Entrante';

-- 3. Movilidades salientes en un periodo
SELECT 
    COUNT(*) AS movilidades_salientes
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_TIEMPO" t ON h.llavetiempo = t.llavetiempo
JOIN datawarehouse."D_MOVILIDAD" m ON h.llavemovilidad = m.llavemovilidad
WHERE t.año = 2025 AND t.semestre = 1
  AND m.direccion = 'Saliente';

--4. Semestre con mayor número de movilidades

SELECT 
    t.año,
    t.semestre,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_TIEMPO" t ON h.llavetiempo = t.llavetiempo
GROUP BY t.año, t.semestre
ORDER BY total_movilidades DESC
LIMIT 1;

--5. Países con mayor cantidad de movilidades (entrantes y salientes)
SELECT 
    l.paisorigen,
    l.paisdestino,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_LUGAR" l ON h.llavelugar = l.llavelugar
GROUP BY l.paisorigen, l.paisdestino
ORDER BY total_movilidades DESC
LIMIT 10;

--6. Países con menor cantidad de movilidades
SELECT 
    l.paisorigen,
    l.paisdestino,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_LUGAR" l ON h.llavelugar = l.llavelugar
GROUP BY l.paisorigen, l.paisdestino
HAVING COUNT(*) > 0
ORDER BY total_movilidades ASC
LIMIT 10;

--7. País que más movilidades realiza hacia la universidad en un periodo
SELECT 
    l.paisorigen,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_LUGAR" l ON h.llavelugar = l.llavelugar
JOIN datawarehouse."D_TIEMPO" t ON h.llavetiempo = t.llavetiempo
WHERE t.año = 2025 AND t.semestre = 1
GROUP BY l.paisorigen
ORDER BY total_movilidades DESC
LIMIT 1;

-- 8.Programa con mayor número de movilidades
SELECT 
    p.nombreprograma,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_PROGRAMA" p ON h.llaveprograma = p.llaveprograma
GROUP BY p.nombreprograma
ORDER BY total_movilidades DESC
LIMIT 1;

-- 9 Programa con menor número de movilidades

SELECT 
    p.nombreprograma,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_PROGRAMA" p ON h.llaveprograma = p.llaveprograma
GROUP BY p.nombreprograma
ORDER BY total_movilidades ASC
LIMIT 1;

-- 10 Programa con mayor constancia (presente en más semestres)

SELECT 
    p.nombreprograma,
    COUNT(DISTINCT t.semestre || '-' || t.año) AS semestres_activos
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_TIEMPO" t ON h.llavetiempo = t.llavetiempo
JOIN datawarehouse."D_PROGRAMA" p ON h.llaveprograma = p.llaveprograma
GROUP BY p.nombreprograma
ORDER BY semestres_activos DESC
LIMIT 1;

-- 11 Tipo de movilidad más realizada

SELECT 
    m.tipo,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_MOVILIDAD" m ON h.llavemovilidad = m.llavemovilidad
GROUP BY m.tipo
ORDER BY total_movilidades DESC
LIMIT 1;

-- 12 Cantidad de movilidades por tipo a lo largo del tiempo
SELECT 
    t.año,
    t.semestre,
    m.tipo,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas"  h
JOIN datawarehouse."D_MOVILIDAD" m ON h.llavemovilidad = m.llavemovilidad
JOIN datawarehouse."D_TIEMPO" t ON h.llavetiempo = t.llavetiempo
GROUP BY t.año, t.semestre, m.tipo
ORDER BY t.año, t.semestre, total_movilidades DESC;

-- 13 Convenio con mayor número de movilidades
SELECT 
    c.tipo,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_CONVENIOS" c ON h.llaveconvenios = c.llaveconvenios
GROUP BY c.tipo
ORDER BY total_movilidades DESC
LIMIT 1;

--14 Entidad que realiza más movilidades por tipo


SELECT 
    l.institucionorigen,
    m.tipo,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_LUGAR" l ON h.llavelugar = l.llavelugar
JOIN datawarehouse."D_MOVILIDAD" m ON h.llavemovilidad = m.llavemovilidad
GROUP BY l.institucionorigen, m.tipo
ORDER BY total_movilidades DESC;

--15 Convenios infrautilizados (vigentes pero con pocas movilidades)

SELECT 
    c.tipo,
    c.vigencia,
    COUNT(h.llaveconvenios) AS total_movilidades
FROM datawarehouse."D_CONVENIOS" c
LEFT JOIN datawarehouse."H_MovilidadesRealizadas" h ON h.llaveconvenios = c.llaveconvenios
WHERE c.estado = 'Activo'
GROUP BY c.tipo, c.vigencia
HAVING COUNT(h.llaveconvenios) < 9  -- umbral configurable
ORDER BY total_movilidades ASC;

-- 16. Distribución por género

SELECT 
    m.genero,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_MOVILIZANTE" m ON h.llavemovilizante = m.llavemovilizante
GROUP BY m.genero
ORDER BY total_movilidades DESC;


-- 17 Promedio de edad de los participantes
SELECT 
    ROUND(AVG(m.edad), 1) AS promedio_edad
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_MOVILIZANTE" m ON h.llavemovilizante = m.llavemovilizante;

-- 18 Distribución de edades según tipo, programa y periodo
SELECT 
    t.año,
    t.semestre,
    p.nombreprograma,
    mo.tipo,
    ROUND(AVG(m.edad), 1) AS promedio_edad,
    COUNT(*) AS total_movilidades
FROM datawarehouse."H_MovilidadesRealizadas" h
JOIN datawarehouse."D_TIEMPO" t ON h.llavetiempo = t.llavetiempo
JOIN datawarehouse."D_PROGRAMA" p ON h.llaveprograma = p.llaveprograma
JOIN datawarehouse."D_MOVILIDAD" mo ON h.llavemovilidad = mo.llavemovilidad
JOIN datawarehouse."D_MOVILIZANTE" m ON h.llavemovilizante = m.llavemovilizante
GROUP BY t.año, t.semestre, p.nombreprograma, mo.tipo
ORDER BY t.año, t.semestre, promedio_edad DESC;


