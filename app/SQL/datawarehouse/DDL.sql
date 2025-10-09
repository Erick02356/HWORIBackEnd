CREATE TABLE datawarehouse."D_TIEMPO" (
    LlaveTiempo INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    Año INTEGER,
    Semestre INTEGER CHECK (Semestre IN (1, 2)),
    Mes INTEGER CHECK (Mes BETWEEN 1 AND 12),
    Dia INTEGER CHECK (Dia BETWEEN 1 AND 31)
);


CREATE TABLE datawarehouse."D_PROGRAMA" (
    LlavePrograma INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    NombrePrograma VARCHAR(150),
    Facultad VARCHAR(150),
    DependenciaAdministrativa VARCHAR(150)
);

CREATE TABLE datawarehouse."D_LUGAR" (
    LlaveLugar INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    PaisOrigen VARCHAR(100),
    PaisDestino VARCHAR(100),
    InstitucionOrigen VARCHAR(150),
    InstitucionDestino VARCHAR(150),
    SedeInstitucion VARCHAR(150)
);

CREATE TABLE datawarehouse."D_MOVILIZANTE" (
    LlaveMovilizante INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    Edad SMALLINT,
    Genero VARCHAR(20),
    EstadoCivil VARCHAR(30),
    Rol VARCHAR(50),
    SemestreCursante SMALLINT
);

CREATE TABLE datawarehouse."D_MOVILIDAD" (
    LlaveMovilidad INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    Tipo VARCHAR(50),
    Modalidad VARCHAR(50),
    Direccion VARCHAR(50),
    DuracionDias INTEGER CHECK (DuracionDias > 0)
);

CREATE TABLE datawarehouse."D_CONVENIOS" (
    LlaveConvenios INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    Tipo VARCHAR(50),
    Vigencia VARCHAR(50),
    Estado VARCHAR(30)
);




CREATE TABLE datawarehouse."H_MovilidadesRealizadas" (
    LlaveHecho       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    LlaveTiempo      INTEGER NOT NULL,
    LlaveConvenios   INTEGER NOT NULL,
    LlaveMovilidad   INTEGER NOT NULL,
    LlaveLugar       INTEGER NOT NULL,
    LlavePrograma    INTEGER NOT NULL,
    LlaveMovilizante INTEGER NOT NULL,
    CONSTRAINT fk_h_tiempo FOREIGN KEY (LlaveTiempo)
        REFERENCES datawarehouse."D_TIEMPO" (LlaveTiempo) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_h_convenios FOREIGN KEY (LlaveConvenios)
        REFERENCES datawarehouse."D_CONVENIOS" (LlaveConvenios) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_h_movilidad FOREIGN KEY (LlaveMovilidad)
        REFERENCES datawarehouse."D_MOVILIDAD" (LlaveMovilidad) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_h_lugar FOREIGN KEY (LlaveLugar)
        REFERENCES datawarehouse."D_LUGAR" (LlaveLugar) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_h_programa FOREIGN KEY (LlavePrograma)
        REFERENCES datawarehouse."D_PROGRAMA" (LlavePrograma) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_h_movilizante FOREIGN KEY (LlaveMovilizante)
        REFERENCES datawarehouse."D_MOVILIZANTE" (LlaveMovilizante) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ------------------------------
-- Índices sobre FKs para rendimiento en joins
-- ------------------------------

CREATE INDEX idx_h_llavetiempo ON datawarehouse."H_MovilidadesRealizadas" (LlaveTiempo);
CREATE INDEX idx_h_llaveconvenios ON datawarehouse."H_MovilidadesRealizadas" (LlaveConvenios);
CREATE INDEX idx_h_llavemovilidad ON datawarehouse."H_MovilidadesRealizadas" (LlaveMovilidad);
CREATE INDEX idx_h_llavelugar ON datawarehouse."H_MovilidadesRealizadas" (LlaveLugar);
CREATE INDEX idx_h_llaveprograma ON datawarehouse."H_MovilidadesRealizadas" (LlavePrograma);
CREATE INDEX idx_h_llavemovilizante ON datawarehouse."H_MovilidadesRealizadas" (LlaveMovilizante);


TRUNCATE TABLE datawarehouse."D_PROGRAMA" 
TRUNCATE TABLE datawarehouse."D_MOVILIZANTE"
TRUNCATE TABLE datawarehouse."D_TIEMPO"
TRUNCATE TABLE datawarehouse."D_MOVILIDAD"
TRUNCATE TABLE datawarehouse."D_LUGAR"

SELECT * FROM  datawarehouse."D_PROGRAMA"
SELECT * FROM  datawarehouse."D_MOVILIZANTE"
SELECT * FROM  datawarehouse."D_TIEMPO"
SELECT * FROM  datawarehouse."D_MOVILIDAD"
SELECT * FROM  datawarehouse."D_LUGAR"

--ALTER SEQUENCE D_PROGRAMA_llaveconvenios_seq RESTART WITH 1;
