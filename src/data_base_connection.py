import os
import sqlite3

# Directorio del archivo connection.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta correcta de la BD
DB_PATH = os.path.join(BASE_DIR, "app.db")

print(">>> USANDO DB_PATH =", DB_PATH)
print(">>> EXISTE? =", os.path.exists(DB_PATH))
print(">>> DIR EXISTE? =", os.path.isdir(os.path.dirname(DB_PATH)))

# def get_connection():
#     return sqlite3.connect(DB_PATH)

def get_connection():
    return sqlite3.connect(
        DB_PATH,
        timeout=10,
        check_same_thread=False
    )
