"""
Backend del login (Flask + SQLite).

Ejecutar:
    pip install -r requirements.txt
    python app.py
Luego abrir http://localhost:5000
"""
import os
import re
import sqlite3
from functools import wraps

from flask import Flask, jsonify, redirect, request, send_from_directory, session
from werkzeug.security import check_password_hash, generate_password_hash

from db import BASE_DIR, DB_PATH, close_db, get_db, now
from mobile import bp as mobile_bp, seed_mobile_data

try:
    import frontend.backend.config as config  # backend/config.py
except ImportError:  # pragma: no cover
    config = None

FRONTEND_DIR = BASE_DIR.parent          # carpeta login_screen (index.html, imágenes)
# Solo se sirven estos tipos de archivo del frontend (nunca .db, .py, .venv, ...)
STATIC_EXTENSIONS = {".html", ".js", ".css", ".jpg", ".jpeg", ".png", ".svg", ".webp", ".ico"}

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID") or getattr(config, "GOOGLE_CLIENT_ID", "")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

app = Flask(__name__, static_folder=None)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "cambia-esta-clave-en-produccion"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)


app.teardown_appcontext(close_db)
app.register_blueprint(mobile_bp)


# ---------------------------------------------------------------- base de datos
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT,
                email         TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at    TEXT NOT NULL,
                last_login    TEXT,
                google_id     TEXT UNIQUE
            )
            """
        )
        # migración para bases creadas con la versión anterior
        cols = [r[1] for r in conn.execute("PRAGMA table_info(users)")]
        if "google_id" not in cols:
            conn.execute("ALTER TABLE users ADD COLUMN google_id TEXT")
        # base de conocimiento de apps móviles (/api/mobile/*)
        seed_mobile_data(conn)


def start_session(db, user_id):
    db.execute("UPDATE users SET last_login = ? WHERE id = ?", (now(), user_id))
    db.commit()
    session.clear()
    session["user_id"] = user_id
    return db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def user_to_dict(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "created_at": row["created_at"],
        "last_login": row["last_login"],
    }


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify(error="No autenticado"), 401
        return view(*args, **kwargs)
    return wrapper


# ---------------------------------------------------------------- API
@app.post("/api/register")
def register():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not EMAIL_RE.match(email):
        return jsonify(error="Email no válido"), 400
    if len(password) < 6:
        return jsonify(error="La contraseña debe tener al menos 6 caracteres"), 400

    db = get_db()
    try:
        cur = db.execute(
            "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (name or None, email, generate_password_hash(password), now()),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify(error="Ese email ya está registrado"), 409

    row = start_session(db, cur.lastrowid)
    return jsonify(message="Usuario registrado", user=user_to_dict(row)), 201


@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    db = get_db()
    row = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    if row is not None and not row["password_hash"]:
        return jsonify(error="Esta cuenta se creó con Google. Usa 'Ingresar con Google'"), 401
    if row is None or not check_password_hash(row["password_hash"], password):
        return jsonify(error="Email o contraseña incorrectos"), 401

    row = start_session(db, row["id"])
    return jsonify(message="Inicio de sesión exitoso", user=user_to_dict(row))


@app.post("/api/google")
def google_login():
    if not GOOGLE_CLIENT_ID:
        return jsonify(error="Google login no configurado: falta GOOGLE_CLIENT_ID en backend/config.py"), 500
    credential = (request.get_json(silent=True) or {}).get("credential")
    if not credential:
        return jsonify(error="Falta el token de Google"), 400

    try:
        from google.auth.transport import requests as google_requests
        from google.oauth2 import id_token
        info = id_token.verify_oauth2_token(credential, google_requests.Request(), GOOGLE_CLIENT_ID)
    except ImportError:
        return jsonify(error="Instala dependencias: pip install -r requirements.txt"), 500
    except ValueError:
        return jsonify(error="Token de Google inválido"), 401

    if not info.get("email_verified"):
        return jsonify(error="El email de Google no está verificado"), 401

    google_id = info["sub"]
    email = info["email"].lower()
    name = info.get("name")

    db = get_db()
    row = db.execute("SELECT * FROM users WHERE google_id = ? OR email = ?", (google_id, email)).fetchone()
    if row is None:
        cur = db.execute(
            "INSERT INTO users (name, email, password_hash, created_at, google_id) VALUES (?, ?, '', ?, ?)",
            (name, email, now(), google_id),
        )
        user_id = cur.lastrowid
    else:
        user_id = row["id"]
        # vincula la cuenta existente (registrada con email) a Google
        db.execute("UPDATE users SET google_id = ?, name = COALESCE(name, ?) WHERE id = ?",
                   (google_id, name, user_id))
    row = start_session(db, user_id)
    return jsonify(message="Inicio de sesión con Google exitoso", user=user_to_dict(row))


@app.get("/api/config")
def public_config():
    return jsonify(google_client_id=GOOGLE_CLIENT_ID)


@app.get("/api/health")
def health():
    return jsonify(status="ok")


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify(message="Sesión cerrada")


@app.get("/api/me")
@login_required
def me():
    row = get_db().execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    if row is None:
        session.clear()
        return jsonify(error="No autenticado"), 401
    return jsonify(user=user_to_dict(row))


# ---------------------------------------------------------------- frontend
@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/home")
def home():
    # Solo usuarios con sesión pueden ver el home
    if "user_id" not in session:
        return redirect("/")
    return send_from_directory(FRONTEND_DIR, "home.html")


@app.get("/<path:filename>")
def static_files(filename):
    # Lista blanca: solo archivos de primer nivel con extensión permitida.
    # (Antes "/Backend/database.db" o "/./backend/database.db" descargaban la base de datos.)
    if "/" in filename or "\\" in filename or os.path.splitext(filename)[1].lower() not in STATIC_EXTENSIONS:
        return jsonify(error="No encontrado"), 404
    if filename == "home.html":
        return redirect("/home")
    return send_from_directory(FRONTEND_DIR, filename)


init_db()

if __name__ == "__main__":
    print("\n  Abre en el navegador: http://localhost:5000  (celular: http://IP-del-computador:5000)\n")
    # 0.0.0.0: también atiende al emulador (10.0.2.2) y al celular en la misma red Wi-Fi
    app.run(host="0.0.0.0", port=5000, debug=True)
