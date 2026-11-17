import os
import re
import sqlite3
import subprocess

from flask import Flask, abort, request

from config import DB_PATH

app = Flask(__name__)

HOSTNAME_RE = re.compile(r"^[A-Za-z0-9.-]{1,253}$")


@app.route("/student")
def get_student():
    name = request.args.get("name", "")
    conn = sqlite3.connect(DB_PATH)
    try:
        # FIXED: parameterized query prevents SQL injection
        rows = conn.execute(
            "SELECT * FROM students WHERE name = ?", (name,)
        ).fetchall()
    finally:
        conn.close()
    return str(rows)


@app.route("/ping")
def ping():
    host = request.args.get("host", "")
    # FIXED: validate input, no shell, argument list
    if not HOSTNAME_RE.match(host) or host.startswith("-"):
        abort(400, "Invalid host")
    result = subprocess.run(
        ["ping", "-c", "1", host],
        capture_output=True, text=True, timeout=5, check=False,
    )
    return result.stdout


if __name__ == "__main__":
    # FIXED: debug controlled by environment, off by default
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")