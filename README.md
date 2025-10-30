# Proyecto - Grado - ORI 2025

## Variables de Entorno

Para ejecutar este proyecto, deberá agregar las siguientes variables de entorno a su archivo .env

`DEBUG` = True

`POSTGRESQL_DB` = yourdatabase

`POSTGRESQL_USER` = youruser

`POSTGRESQL_PASSWORD` = yourpassword

`POSTGRESQL_HOST` = 127.0.0.1

`JWT_SECRET_KEY` = clavesecreta
`JWT_ALG`=HS256

`PASSWORD_RESET_EXPIRES_MIN`=15
`FRONTEND_RESET_URL`=http://localhost:yourPort/auth/reset-password
#email
`EMAIL_ENABLED`=true
`SMTP_HOST`=smtp.gmail.com
`SMTP_PORT`=your port
`SMTP_USER`=your user
`SMTP_PASS`= your aplication pass
`SMTP_FROM`= email por donde se enviará
`SMTP_USE_TLS`=true
`SMTP_USE_SSL`=false
#n8n
`N8N_WEBHOOK_URL`=http://localhost:yourPort/webhook-test/ingesta-excel
`MAX_UPLOAD_MB`=25
`N8N_DOWNLOAD_WEBHOOK_URL`=http://localhost:yourPort/webhook-test/snies/download
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
