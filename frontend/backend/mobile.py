"""
API interna de conocimiento sobre aplicaciones móviles (/api/mobile/*).

Todas las rutas requieren sesión iniciada. El contenido vive en mobile_data.py
y se vuelca a SQLite al arrancar con seed_mobile_data().
"""
import json
import unicodedata

from flask import Blueprint, jsonify, request, session

import mobile_data as mobile_data
from db import get_db

bp = Blueprint("mobile", __name__, url_prefix="/api/mobile")

# columnas que se guardan como JSON (listas)
JSON_FIELDS = {"languages", "package_formats", "key_points", "platforms", "pros", "cons", "tags"}


# ---------------------------------------------------------------- esquema y datos
def init_mobile_tables(conn):
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS mobile_platforms (
            slug TEXT PRIMARY KEY, name TEXT NOT NULL, vendor TEXT, languages TEXT, ide TEXT,
            store TEXT, package_formats TEXT, developer_fee TEXT, market_share TEXT,
            summary TEXT, key_points TEXT
        );
        CREATE TABLE IF NOT EXISTS mobile_frameworks (
            slug TEXT PRIMARY KEY, name TEXT NOT NULL, type TEXT, company TEXT, language TEXT,
            platforms TEXT, first_release TEXT, summary TEXT, pros TEXT, cons TEXT, use_when TEXT
        );
        CREATE TABLE IF NOT EXISTS mobile_articles (
            slug TEXT PRIMARY KEY, title TEXT NOT NULL, category TEXT, level TEXT, tags TEXT,
            summary TEXT, content TEXT
        );
        CREATE TABLE IF NOT EXISTS mobile_glossary (
            slug TEXT PRIMARY KEY, term TEXT NOT NULL, definition TEXT NOT NULL
        );
        """
    )


def _replace_all(conn, table, rows):
    """Sustituye el contenido de la tabla por `rows` (lista de dicts)."""
    conn.execute(f"DELETE FROM {table}")
    for row in rows:
        values = {k: json.dumps(v, ensure_ascii=False) if k in JSON_FIELDS else v for k, v in row.items()}
        cols = ", ".join(values)
        marks = ", ".join("?" for _ in values)
        conn.execute(f"INSERT INTO {table} ({cols}) VALUES ({marks})", tuple(values.values()))


def seed_mobile_data(conn):
    init_mobile_tables(conn)
    _replace_all(conn, "mobile_platforms", mobile_data.PLATFORMS)
    _replace_all(conn, "mobile_frameworks", mobile_data.FRAMEWORKS)
    _replace_all(conn, "mobile_articles", mobile_data.ARTICLES)
    _replace_all(conn, "mobile_glossary",
                 [{"slug": s, "term": t, "definition": d} for s, t, d in mobile_data.GLOSSARY])


# ---------------------------------------------------------------- utilidades
def _to_dict(row):
    return {k: json.loads(row[k]) if k in JSON_FIELDS and row[k] else row[k] for k in row.keys()}


def _normalize(text):
    """Minúsculas y sin tildes, para que 'autenticacion' encuentre 'Autenticación'."""
    text = unicodedata.normalize("NFKD", str(text).lower())
    return "".join(c for c in text if not unicodedata.combining(c))


def _matches(item, q):
    return q in _normalize(" ".join(str(v) for v in item.values()))


def _fetch(table, order="name", where="", params=()):
    sql = f"SELECT * FROM {table} {where} ORDER BY {order}"
    return [_to_dict(r) for r in get_db().execute(sql, params)]


def _get_one(table, slug, label):
    row = get_db().execute(f"SELECT * FROM {table} WHERE slug = ?", (slug,)).fetchone()
    if row is None:
        return jsonify(error=f"No se encontró: {label} '{slug}'"), 404
    return jsonify(_to_dict(row))


def _filter_by_query(items):
    q = _normalize(request.args.get("q", "").strip())
    return [i for i in items if _matches(i, q)] if q else items


@bp.before_request
def require_login():
    if "user_id" not in session:
        return jsonify(error="No autenticado"), 401


# ---------------------------------------------------------------- rutas
@bp.get("/overview")
def overview():
    db = get_db()
    count = lambda t: db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]  # noqa: E731
    categories = [r[0] for r in db.execute("SELECT DISTINCT category FROM mobile_articles ORDER BY category")]
    types = [r[0] for r in db.execute("SELECT DISTINCT type FROM mobile_frameworks ORDER BY type")]
    return jsonify(
        platforms=count("mobile_platforms"),
        frameworks=count("mobile_frameworks"),
        articles=count("mobile_articles"),
        glossary_terms=count("mobile_glossary"),
        article_categories=categories,
        framework_types=types,
    )


@bp.get("/platforms")
def platforms():
    return jsonify(items=_filter_by_query(_fetch("mobile_platforms")))


@bp.get("/platforms/<slug>")
def platform_detail(slug):
    return _get_one("mobile_platforms", slug, "plataforma")


@bp.get("/frameworks")
def frameworks():
    """Filtros opcionales: ?type=nativo|multiplataforma|híbrido &platform=iOS &q=texto"""
    items = _fetch("mobile_frameworks")
    if fw_type := request.args.get("type"):
        items = [i for i in items if _normalize(i["type"]) == _normalize(fw_type)]
    if platform := request.args.get("platform"):
        items = [i for i in items if _normalize(platform) in map(_normalize, i["platforms"])]
    return jsonify(items=_filter_by_query(items))


@bp.get("/frameworks/<slug>")
def framework_detail(slug):
    return _get_one("mobile_frameworks", slug, "framework")


@bp.get("/articles")
def articles():
    """Filtros opcionales: ?category= &level= &tag= &q=. El listado no incluye el contenido completo."""
    items = _fetch("mobile_articles", order="category, title")
    for field in ("category", "level"):
        if value := request.args.get(field):
            items = [i for i in items if _normalize(i[field]) == _normalize(value)]
    if tag := request.args.get("tag"):
        items = [i for i in items if _normalize(tag) in map(_normalize, i["tags"])]
    items = _filter_by_query(items)
    return jsonify(items=[{k: v for k, v in i.items() if k != "content"} for i in items])


@bp.get("/articles/<slug>")
def article_detail(slug):
    return _get_one("mobile_articles", slug, "artículo")


@bp.get("/glossary")
def glossary():
    return jsonify(items=_filter_by_query(_fetch("mobile_glossary", order="term")))


@bp.get("/search")
def search():
    """Búsqueda global: ?q=texto (mínimo 2 caracteres)."""
    q = _normalize(request.args.get("q", "").strip())
    if len(q) < 2:
        return jsonify(error="El parámetro q debe tener al menos 2 caracteres"), 400

    sources = [
        ("platform", "mobile_platforms", "name"),
        ("framework", "mobile_frameworks", "name"),
        ("article", "mobile_articles", "title"),
        ("glossary", "mobile_glossary", "term"),
    ]
    results = []
    for kind, table, title_field in sources:
        for item in _fetch(table, order=title_field):
            if _matches(item, q):
                results.append({
                    "type": kind,
                    "slug": item["slug"],
                    "title": item[title_field],
                    "summary": item.get("summary") or item.get("definition"),
                })
    return jsonify(query=request.args["q"], total=len(results), results=results)
