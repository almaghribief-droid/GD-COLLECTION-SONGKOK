import os
import sqlite3
from functools import wraps
from flask import Flask, request, jsonify, session, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(BASE_DIR, "jarvis.db"))
APP_PASSWORD = os.environ.get("APP_PASSWORD")
SECRET_KEY = os.environ.get("SECRET_KEY")

app = Flask(__name__, static_folder="static")
app.secret_key = SECRET_KEY or "development-only-change-this"
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "1") == "1",
)

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                phone TEXT DEFAULT '',
                product TEXT DEFAULT '',
                quantity INTEGER DEFAULT 1,
                status TEXT DEFAULT 'Baru',
                notes TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("authenticated"):
            return jsonify({"error": "Silakan login terlebih dahulu."}), 401
        return fn(*args, **kwargs)
    return wrapper

@app.get("/")
def home():
    return send_from_directory("static", "index.html")

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "app": "GD COLLECTION JARVIS", "stage": "starter-backend"})

@app.post("/api/login")
def login():
    if not APP_PASSWORD or not SECRET_KEY:
        return jsonify({"error": "Server belum dikonfigurasi. Atur APP_PASSWORD dan SECRET_KEY."}), 503
    data = request.get_json(silent=True) or {}
    if data.get("password") != APP_PASSWORD:
        return jsonify({"error": "Kata sandi tidak cocok."}), 401
    session.clear()
    session["authenticated"] = True
    return jsonify({"ok": True})

@app.post("/api/logout")
@login_required
def logout():
    session.clear()
    return jsonify({"ok": True})

@app.get("/api/leads")
@login_required
def list_leads():
    with db() as conn:
        rows = conn.execute(
            "SELECT id, customer_name, phone, product, quantity, status, notes, created_at FROM leads ORDER BY id DESC"
        ).fetchall()
    return jsonify([dict(row) for row in rows])

@app.post("/api/leads")
@login_required
def add_lead():
    data = request.get_json(silent=True) or {}
    name = str(data.get("customer_name", "")).strip()
    if not name:
        return jsonify({"error": "Nama pelanggan wajib diisi."}), 400
    try:
        quantity = max(1, int(data.get("quantity", 1)))
    except (TypeError, ValueError):
        return jsonify({"error": "Jumlah harus berupa angka."}), 400
    with db() as conn:
        cur = conn.execute(
            "INSERT INTO leads (customer_name, phone, product, quantity, status, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (name, str(data.get("phone", ""))[:40], str(data.get("product", ""))[:120],
             quantity, str(data.get("status", "Baru"))[:40], str(data.get("notes", ""))[:1000])
        )
        lead_id = cur.lastrowid
    return jsonify({"ok": True, "id": lead_id}), 201

@app.get("/api/products")
@login_required
def products():
    return jsonify([
        {"name": "Kontesa non-AC", "reference_price_idr": 17000},
        {"name": "Kontesa AC", "reference_price_idr": 20000},
        {"name": "Kontesa full AC", "reference_price_idr": 22000},
        {"name": "Royal floking non-AC", "reference_price_idr": 26000},
        {"name": "Royal floking AC", "reference_price_idr": 29000},
        {"name": "Royal floking full AC", "reference_price_idr": 31000}
    ])

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
