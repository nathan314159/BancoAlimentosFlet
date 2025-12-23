import os
import sqlite3
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta correcta de la BD
DB_PATH = os.path.join(BASE_DIR, "app.db")

API_URL = "http://localhost/bancoAlimentos/sync-encuesta"

def mapear_encuesta(cursor, encuesta):
    if cursor.description is None:
        return None

    columnas = [col[0] for col in cursor.description]
    return dict(zip(columnas, encuesta))


def sincronizar_encuestas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM tbl_datos_generales_PRUEBA
        WHERE sincronizado = 0
    """)
    encuestas = cursor.fetchall()

    print("📤 Encuestas pendientes:", len(encuestas))

    for encuesta in encuestas:
        data = mapear_encuesta(cursor, encuesta)
        if data is None:
            return

        try:
            response = requests.post(API_URL, json=data, timeout=10)

            if response.status_code == 200:
                cursor.execute("""
                    UPDATE tbl_datos_generales_PRUEBA
                    SET sincronizado = 1
                    WHERE uuid = ?
                """, (data["uuid"],))

                conn.commit()
                print("✅ Sincronizada:", data["uuid"])

            else:
                print("❌ Error servidor:", response.text)

        except Exception as e:
            print("🚫 Sin internet:", e)
            break

    conn.close()
