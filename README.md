
# Proyecto - Grado - ORI 2025
## Variables de Entorno

Para ejecutar este proyecto, deberá agregar las siguientes variables de entorno a su archivo .env

`DEBUG` = True

`POSTGRESQL_DB` = yourdatabase

`POSTGRESQL_USER` = youruser

`POSTGRESQL_PASSWORD` = yourpassowrd

`POSTGRESQL_HOST` = 127.0.0.1

`JWT_SECRET_KEY` = clavesecreta

## Despliegue

Crea un entorno virtual
```bash
# windows
python -m venv venv

#linux
sudo python3 -m venv venv
```
Activar el Entorno Virtual
```bash
# windows
.\venv\Scripts\activate

# linux
source venv/bin/activate

```
Instalar dependencias
```bash
# windows
pip install -r requirements.txt

# linux
pip3 install -r requirements.txt

```
Correr Aplicación
```bash
uvicorn main:app --reload --port 8888
```





