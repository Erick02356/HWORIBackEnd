create or replace procedure datawarehouse.poblar_hecho_movilidades()
language plpgsql
as $$
begin
    insert into datawarehouse."H_MovilidadesRealizadas" (
        "llavetiempo",
        "llaveconvenios",
        "llavemovilidad",
        "llavelugar",
        "llaveprograma",
        "llavemovilizante"
    )
    select
        t."llavetiempo",
        m."llavemovilidad",
        l."llavelugar",
        p."llaveprograma",
        mo."llavemovilizante",
        c."llaveconvenios"
    from parameters.vw_stg_movilidades_enriquecida s
    inner join datawarehouse."D_TIEMPO" t
        on t."año" = s."ano" and t."semestre" = s."semestre" 
        and t."mes" = s."mes" and t."dia" = s."dia"
    inner join datawarehouse."D_MOVILIDAD" m
        on m."tipo" = s."tipomovilidad"
        and m."modalidad" = s."modalidad"
        and m."direccion" = s."direccion"
        and m."duraciondias" = s."duraciondias"
    inner join datawarehouse."D_LUGAR" l
        on l."paisorigen" = s."paisorigen"
        and l."paisdestino" = s."paisdestino"
        and l."institucionorigen" = s."institucionorigen"
        and l."instituciondestino" = s."instituciondestino"
    inner join datawarehouse."D_PROGRAMA" p
        on p."nombreprograma" = s."nombreprograma"
        and p."facultad" = s."facultad"
        and p."dependenciaadministrativa" = s."dependenciaadministrativa"
    inner join datawarehouse."D_MOVILIZANTE" mo
        on mo."edad" = s."edad"
        and mo."genero" = s."genero"
        and mo."estadocivil" = s."estadocivil"
        and mo."rol" = s."rol"
        and (mo."semestrecursante" = s."semestrecursante" or s."semestrecursante" is null)
    inner join datawarehouse."D_CONVENIOS" c
        on c."tipo" = s."TipoConvenio"
        and c."vigencia" = s."VigenciaConvenio"
        and c."estado" = s."EstadoConvenio"
    on conflict do nothing;
end;
$$;

CALL datawarehouse.poblar_hecho_movilidades()
----v2
CREATE OR REPLACE PROCEDURE datawarehouse.poblar_hecho_movilidades2()
LANGUAGE plpgsql
AS $$
BEGIN
  -- si quieres carga full:
  TRUNCATE TABLE datawarehouse."H_MovilidadesRealizadas" RESTART IDENTITY CASCADE;

  INSERT INTO datawarehouse."H_MovilidadesRealizadas" (
    "llavetiempo",
    "llaveconvenios",
    "llavemovilidad",
    "llavelugar",
    "llaveprograma",
    "llavemovilizante"
  )
  WITH
  t_dedup AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY "año","semestre","mes","dia" ORDER BY "llavetiempo") rn
    FROM datawarehouse."D_TIEMPO"
  ),
  mov_dedup AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY "tipo","modalidad","direccion","duraciondias" ORDER BY "llavemovilidad") rn
    FROM datawarehouse."D_MOVILIDAD"
  ),
  lug_dedup AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY "paisorigen","paisdestino","institucionorigen","instituciondestino","sedeinstitucion" ORDER BY "llavelugar") rn
    FROM datawarehouse."D_LUGAR"
  ),
  prog_dedup AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY "nombreprograma","facultad","dependenciaadministrativa" ORDER BY "llaveprograma") rn
    FROM datawarehouse."D_PROGRAMA"
  ),
  mo_dedup AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY "edad","genero","estadocivil","rol","semestrecursante" ORDER BY "llavemovilizante") rn
    FROM datawarehouse."D_MOVILIZANTE"
  ),
  conv_dedup AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY "tipo","vigencia","estado" ORDER BY "llaveconvenios") rn
    FROM datawarehouse."D_CONVENIOS"
  )
  SELECT DISTINCT
    t."llavetiempo",         -- 1) TIEMPO
    c."llaveconvenios",      -- 2) CONVENIO  ✅ ahora va segundo
    m."llavemovilidad",      -- 3) MOVILIDAD
    l."llavelugar",          -- 4) LUGAR
    p."llaveprograma",       -- 5) PROGRAMA
    mo."llavemovilizante"    -- 6) MOVILIZANTE
  FROM parameters.vw_stg_movilidades_enriquecida s
  INNER JOIN t_dedup    t  
	  ON t."año"=s."ano" AND t."semestre"=s."semestre" 
	  AND t."mes"=s."mes" AND t."dia"=s."dia" AND t.rn=1
  INNER JOIN mov_dedup  m  
	  ON m."tipo"=s."tipomovilidad" AND m."modalidad"=s."modalidad" 
	  AND m."direccion"=s."direccion" AND m."duraciondias"=s."duraciondias" AND m.rn=1
  INNER JOIN lug_dedup  l  
	  ON l."paisorigen"=s."paisorigen" AND l."paisdestino"=s."paisdestino" 
	  AND l."institucionorigen"=s."institucionorigen" 
	  AND l."instituciondestino"=s."instituciondestino"
	  AND l."sedeinstitucion"=s."sedeinstitucion" AND l.rn=1
  INNER JOIN prog_dedup p  
	  ON p."nombreprograma"=s."nombreprograma" AND p."facultad"=s."facultad" 
	  AND p."dependenciaadministrativa"=s."dependenciaadministrativa" AND p.rn=1
  INNER JOIN mo_dedup  mo 
	  ON mo."edad"=s."edad" AND mo."genero"=s."genero" 
	  AND mo."estadocivil"=s."estadocivil" AND mo."rol"=s."rol"
	   AND COALESCE(mo."semestrecursante",-1)=COALESCE(s."semestrecursante",-1) AND mo.rn=1
  INNER JOIN conv_dedup c  
  ON c."tipo"=s."TipoConvenio" AND c."vigencia"=s."VigenciaConvenio" 
  AND c."estado"=s."EstadoConvenio" AND c.rn=1;
END;
$$;
