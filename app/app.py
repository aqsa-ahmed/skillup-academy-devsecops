import sqlite3
import subprocess
from flask import Flask, request

app = Flask(__name__)

@app.route("/student")
def get_student():
    name = request.args.get("name")
    conn = sqlite3.connect("students.db")
    # VULNERABLE: SQL injection (string-built query)
    query = "SELECT * FROM students WHERE name = '%s'" % name
    return str(conn.execute(query).fetchall())

@app.route("/ping")
def ping():
    host = request.args.get("host")
    # VULNERABLE: command injection (shell=True with user input)
    return subprocess.check_output("ping -c 1 " + host, shell=True)

if __name__ == "__main__":
    app.run(debug=True)  # VULNERABLE: debug mode exposed
