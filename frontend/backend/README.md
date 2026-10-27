# Login con backend (Python + Flask + SQLite)

## Ejecutar (Windows)
```
cd C:\Users\Innovacion01\Desktop\login_screen
python -m venv .venv
.venv\Scripts\activate
pip install -r backend\requirements.txt
cd backend
python app.py
```
Deja esa terminal abierta y abre http://localhost:5000 en el navegador.
Desde el emulador de Android Studio: http://10.0.2.2:5000
Desde un celular en la misma Wi-Fi: http://IP-del-computador:5000 (ipconfig -> IPv4)

La base `database.db` se crea sola en backend/ (tabla `users`, contraseñas con hash).

## Login con Google
1. https://console.cloud.google.com -> crea o elige un proyecto.
2. APIs y servicios > Pantalla de consentimiento de OAuth: Externo, nombre y correo.
3. APIs y servicios > Credenciales > Crear credenciales > ID de cliente de OAuth
   - Tipo: Aplicación web
   - Orígenes autorizados de JavaScript: http://localhost y http://localhost:5000
4. Copia el ID de cliente y pégalo en backend/config.py:
   GOOGLE_CLIENT_ID = "1234-abc.apps.googleusercontent.com"
5. Reinicia python app.py. El botón de Google aparece en el login.
El botón de Google solo funciona en localhost o en un dominio real: desde el celular por IP, Google lo rechaza.

## API
| Método | Ruta | Body JSON |
|---|---|---|
| POST | /api/register | name, email, password |
| POST | /api/login | email, password |
| POST | /api/google | credential (token de Google) |
| POST | /api/logout | — |
| GET | /api/me | — (requiere sesión) |
| GET | /api/config | — (Client ID de Google) |
| GET | /home | página protegida |
| GET | /api/mobile/... | base de conocimiento (requiere sesión); ver mobile.py |
