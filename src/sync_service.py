import os
import sqlite3
import requests

# -------------------------
# CONFIGURACIÓN
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")
API_URL = "http://localhost/bancoAlimentos/sync-encuesta"

# -------------------------
# FUNCIÓN AUXILIAR
# -------------------------
def buscar_id_catalogo(cursor, nombre, id_catalogo):
    """
    Busca el id_item en tbl_item_catalogo según el nombre y el catálogo.
    Retorna None si no encuentra.
    """
    if not nombre:
        return None

    cursor.execute("""
        SELECT id_item
        FROM tbl_item_catalogo
        WHERE itc_nombre LIKE ?
          AND id_catalogo = ?
          AND itc_estado = 1
    """, (f"%{nombre}%", id_catalogo))

    row = cursor.fetchone()
    return row[0] if row else None

# -------------------------
# SINCRONIZAR ENCUESTAS
# -------------------------
def sincronizar_encuestas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Obtener encuestas no sincronizadas
    cursor.execute("""
        SELECT *
        FROM tbl_datos_generales_PRUEBA
        WHERE sincronizado = 0
    """)

    columnas = [col[0] for col in cursor.description]
    encuestas = cursor.fetchall()

    print("📤 Encuestas pendientes:", len(encuestas))

    for encuesta in encuestas:
        data = dict(zip(columnas, encuesta))

        # -------------------------
        # 🔍 MAPEAR UBICACIÓN
        # -------------------------
        provincia_id = buscar_id_catalogo(
            cursor,
            data.get("datos_provincia"),
            18
        )

        canton_id = buscar_id_catalogo(
            cursor,
            data.get("datos_canton"),
            19
        )

        parroquia_id = buscar_id_catalogo(
            cursor,
            data.get("datos_parroquias"),
            20
        )
        
        tipo_parroquia_id = None

        if parroquia_id:
            tipo_parroquia_id = 20  # ejemplo: urbana

        # 🔎 DEBUG (puedes quitar luego)
        print("🔎 Provincia:", data.get("datos_provincia"), "→", provincia_id)
        print("🔎 Cantón:", data.get("datos_canton"), "→", canton_id)
        print("🔎 Parroquia:", data.get("datos_parroquias"), "→", parroquia_id)

        # -------------------------
        # 📦 JSON PARA API
        # -------------------------
        data_api = {
            "uuid": data.get("uuid"),
            "datos_cedula_voluntario": data.get("datos_cedula_voluntario"),

            "provincia": provincia_id,
            "canton": canton_id,
            "parroquia": parroquia_id,
            "tipo_parroquia": tipo_parroquia_id,

            "datos_comunidades": data.get("datos_comunidades"),
            "datos_barrios": data.get("datos_barrios"),
            "datos_tipo_viviendas": data.get("datos_tipo_viviendas"),
            "datos_techos": data.get("datos_techos"),
            "datos_paredes": data.get("datos_paredes"),
            "datos_pisos": data.get("datos_pisos"),

            "datos_cuarto": data.get("datos_cuarto"),
            "datos_combustibles_cocina": data.get("datos_combustibles_cocina"),
            "datos_servicios_higienicos": data.get("datos_servicios_higienicos"),
            "datos_viviendas": data.get("datos_viviendas"),
            "datos_pago_vivienda": data.get("datos_pago_vivienda"),
            "datos_agua": data.get("datos_agua"),
            "datos_pago_agua": data.get("datos_pago_agua"),
            "datos_pago_luz": data.get("datos_pago_luz"),
            "datos_cantidad_luz": data.get("datos_cantidad_luz"),
            "datos_internet": data.get("datos_internet"),
            "datos_pago_internet": data.get("datos_pago_internet"),
            "datos_tv_cable": data.get("datos_tv_cable"),
            "datos_tv_pago": data.get("datos_tv_pago"),
            "datos_eliminacion_basura": data.get("datos_eliminacion_basura"),
            "datos_lugares_viveres": data.get("datos_lugares_mayor_frecuencia_viveres"),
            "datos_gastos_viveres": data.get("datos_gastos_viveres_alimentacion"),
            "datos_medio_transporte": data.get("datos_medio_transporte"),
            "datos_estado_transporte": data.get("datos_estado_transporte"),
            "datos_terrenos": data.get("datos_terrenos"),
            "datos_celular": data.get("datos_celular"),
            "datos_cantidad_celulare": data.get("datos_cantidad_celulare"),
            "datos_plan_celular": data.get("datos_plan_celular"),
            "datos_observacion": data.get("datos_observacion"),
            "datos_consentimiento": data.get("datos_consentimiento"),

            "familiares": data.get("familiares", [])
        }

        print("📨 JSON enviado:", data_api)

        # -------------------------
        # 🌐 ENVIAR A API
        # -------------------------
        try:
            response = requests.post(API_URL, json=data_api, timeout=10)

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
            print("🚫 Error de conexión:", e)
            break

    conn.close()

# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    sincronizar_encuestas()
