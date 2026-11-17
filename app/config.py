import os

# FIXED: secrets come from environment variables, never from source code
SECRET_KEY = os.environ["SECRET_KEY"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PATH = os.environ.get("DB_PATH", "students.db")