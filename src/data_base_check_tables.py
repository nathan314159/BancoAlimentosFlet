import sqlite3

# Nombre del archivo SQLite
DB_NAME = "app.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("\nTablas encontradas en", DB_NAME + ":")
for t in tables:
    print(" -", t[0])

conn.close()
