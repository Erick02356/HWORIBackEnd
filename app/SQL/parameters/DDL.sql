CREATE TABLE IF NOT EXISTS parameters.usuarios
(
    id integer NOT NULL DEFAULT nextval('parameters.usuarios_id_seq'::regclass),
    usuario character varying(100) COLLATE pg_catalog."default" NOT NULL,
    password character varying(255) COLLATE pg_catalog."default" NOT NULL,
    nombre character varying(150) COLLATE pg_catalog."default",
    correo character varying(255) COLLATE pg_catalog."default",
    rol parameters.rol_usuario_enum NOT NULL DEFAULT 'coordinador'::parameters.rol_usuario_enum,
    estado parameters.estado_usuario_enum NOT NULL DEFAULT 'Activo'::parameters.estado_usuario_enum,
    ultimo_acceso timestamp with time zone,
    creado_en timestamp with time zone NOT NULL DEFAULT now(),
    actualizado_en timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT usuarios_pkey PRIMARY KEY (id),
    CONSTRAINT usuarios_correo_key UNIQUE (correo),
    CONSTRAINT usuarios_usuario_key UNIQUE (usuario)
)