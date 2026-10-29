import os
import time

import psycopg
from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["POSTGRES_DB"]
DB_USER = os.environ["POSTGRES_USER"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DEMO_USER = os.environ["DEMO_USERNAME"]
DEMO_PASSWORD = os.environ["DEMO_PASSWORD"]


def connect_db():
    return psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=3,
    )


def initialize_database():
    for attempt in range(30):
        try:
            with connect_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            username TEXT UNIQUE NOT NULL,
                            password_hash TEXT NOT NULL
                        )
                    """)
                    cur.execute(
                        """
                        INSERT INTO users (username, password_hash)
                        VALUES (%s, %s)
                        ON CONFLICT (username) DO NOTHING
                        """,
                        (DEMO_USER, generate_password_hash(DEMO_PASSWORD)),
                    )
            return
        except psycopg.OperationalError:
            if attempt == 29:
                raise
            time.sleep(2)


initialize_database()


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify(message="Invalid request"), 400

    try:
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT password_hash FROM users WHERE username = %s",
                    (username,),
                )
                row = cur.fetchone()
    except psycopg.Error:
        app.logger.exception("Database query failed")
        return jsonify(message="Service temporarily unavailable"), 503

    if row and check_password_hash(row[0], password):
        return jsonify(message="Login successful!")

    return jsonify(message="Invalid username or password"), 401
