

-- Tabla PAIS
CREATE TABLE operations."pais" (
    codigo_iso VARCHAR(3) PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    codigo_iso2 VARCHAR(2),
    codigo_iso3 VARCHAR(3)
);
select * from operations."pais"
-- Tabla INSTITUCION
CREATE TABLE  operations."institucion" (
    codigo VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    direccion VARCHAR(300),
    representante_legal VARCHAR(150),
    correo VARCHAR(150),
    telefono VARCHAR(50),
    codigo_pais VARCHAR(3) NOT NULL,
    CONSTRAINT fk_institucion_pais FOREIGN KEY (codigo_pais)
        REFERENCES  operations."pais" (codigo_iso)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Tabla CONVENIO
CREATE TABLE  operations."convenio" (
    codigo VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    tipo VARCHAR(100),
    fecha_inicio DATE,
    fecha_inicializacion DATE,
    estado VARCHAR(50),
    codigo_institucion VARCHAR(50) NOT NULL,
    CONSTRAINT fk_convenio_institucion FOREIGN KEY (codigo_institucion)
        REFERENCES  operations."institucion" (codigo)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Tabla TIPO_MOVILIDAD
CREATE TABLE operations."tipo_movilidad" (
    codigo VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL
);

-- Tabla intermedia CONVENIO_TIPO_MOVILIDAD con PK compuesta
CREATE TABLE operations."convenio_tipo_movilidad" (
    convenio_codigo VARCHAR(50) NOT NULL,
    tipo_movilidad_codigo VARCHAR(50) NOT NULL,
    -- Clave primaria compuesta
    CONSTRAINT pk_convenio_tipo_movilidad PRIMARY KEY (convenio_codigo, tipo_movilidad_codigo),
    -- Llaves foráneas
    CONSTRAINT fk_ctm_convenio FOREIGN KEY (convenio_codigo)
        REFERENCES operations."convenio" (codigo)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_ctm_tipomov FOREIGN KEY (tipo_movilidad_codigo)
        REFERENCES operations."tipo_movilidad" (codigo)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Índices recomendados
CREATE INDEX idx_institucion_pais ON institucion (codigo_pais);
CREATE INDEX idx_convenio_institucion ON convenio (codigo_institucion);
CREATE INDEX idx_ctm_convenio ON convenio_tipo_movilidad (convenio_codigo);
CREATE INDEX idx_ctm_tipomov ON convenio_tipo_movilidad (tipo_movilidad_codigo);


-----Falto el campo estado evitando así eliminado fisico
ALTER TABLE operations.institucion
ADD COLUMN estado VARCHAR(20) DEFAULT 'Activo';

-- Asegurar que todos los registros existentes tengan valor 'Activo'
UPDATE operations.institucion
SET estado = 'Activo'
WHERE estado IS NULL;

--  Evitar valores nulos en el futuro
ALTER TABLE operations.institucion
ALTER COLUMN estado SET NOT NULL;