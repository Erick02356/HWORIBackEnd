CREATE OR REPLACE VIEW operations."v_d_convenios" AS
SELECT DISTINCT 
    tipo,
    (fecha_inicializacion - fecha_inicio) AS Vigencia,
    estado
FROM operations."convenio";


INSERT INTO datawarehouse."D_CONVENIOS"(tipo,vigencia,estado)
SELECT tipo, vigencia, estado FROM operations."v_d_convenios"


select * from datawarehouse."D_CONVENIOS"


--- V2
-- First, create a function that will handle the refresh logic
CREATE OR REPLACE FUNCTION operations.refresh_d_convenios()
RETURNS TRIGGER AS $$
BEGIN
    -- Truncate the dimension table
    TRUNCATE TABLE datawarehouse."D_CONVENIOS";
    
    -- Re-insert all data from the view
    INSERT INTO datawarehouse."D_CONVENIOS"(tipo, vigencia, estado)
    SELECT tipo, vigencia, estado FROM operations."v_d_convenios";
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger that fires after insert on convenio table
CREATE OR REPLACE TRIGGER tr_refresh_d_convenios
    AFTER INSERT ON operations."convenio"
    FOR EACH STATEMENT
    EXECUTE FUNCTION operations.refresh_d_convenios();