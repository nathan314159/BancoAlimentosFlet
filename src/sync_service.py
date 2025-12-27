import os
import sqlite3
import httpx
from helper import *

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
        WHERE LOWER(itc_nombre) LIKE LOWER(?)
          AND id_catalogo = ?
          AND itc_estado = 1
        LIMIT 1
    """, (f"%{nombre.strip()}%", id_catalogo))

    row = cursor.fetchone()
    return row[0] if row else None


def obtener_familiares(cursor, id_datos_generales):
    cursor.execute("""
        SELECT
            dp.datos_parentesco_nombres,
            dp.datos_parentesco_apellidos,
            dp.datos_parentesco_documento,
            dp.datos_parentesco_celular_telf,
            dp.datos_parentesco_etnia,
            dp.datos_parentesco_genero,
            dp.datos_parentesco_nivel_educacion,
            dp.datos_parentesco_fecha_de_nacimiento,
            dp.datos_parentesco_edad,
            dp.datos_parentesco_estado_civil,
            dp.datos_parentesco_discapacidad,
            dp.datos_parentesco_enfermedad_catastrofica,
            dp.datos_parentesco_trabaja,
            dp.datos_parentesco_ocupacion,
            dp.datos_parentesco_ingreso_mensual,
            dp.datos_parentesco_parentesco
        FROM tbl_datos_parentesco dp
        JOIN tbl_datos_generales_parentesco dgp
          ON dp.id_datos_parentesco = dgp.id_datos_parentescos
        WHERE dgp.id_datos_generales = ?
    """, (id_datos_generales,))

    familiares = []

    for row in cursor.fetchall():
        familiares.append({
            "nombres": row[0],
            "apellidos": row[1],
            "documento": row[2],
            "telefono": row[3],
            "etnia": row[4],
            "genero": row[5],
            "nivel_educacion": row[6],
            "fecha_nacimiento": row[7],
            "edad": row[8],
            "estado_civil": row[9],
            "discapacidad": row[10],
            "enfermedad": row[11],
            "trabaja": row[12],
            "ocupacion": row[13],
            "ingreso": row[14],
            "parentesco": row[15],
        })

    return familiares


# -------------------------
# SINCRONIZAR ENCUESTAS
# -------------------------
def sincronizar_encuestas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

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
        # 👨‍👩‍👧 FAMILIARES → CONVERTIR A IDS
        # -------------------------
        familiares_raw = obtener_familiares(cursor, data["id_datos_generales"])
        familiares = []

        for fam in familiares_raw:
            familiares.append({
                "nombres": fam.get("nombres"),
                "apellidos": fam.get("apellidos"),
                "documento": fam.get("documento"),
                "telefono": fam.get("telefono"),

                # 🔁 TEXTO → ID
                "etnia": buscar_id_catalogo(cursor, fam.get("etnia"), 34),
                "genero": buscar_id_catalogo(cursor, fam.get("genero"), 35),
                "nivel_educacion": buscar_id_catalogo(cursor, fam.get("nivel_educacion"), 36),
                "estado_civil": buscar_id_catalogo(cursor, fam.get("estado_civil"), 37),

                "fecha_nacimiento": fam.get("fecha_nacimiento"),
                "edad": int(fam.get("edad", 0)) if fam.get("edad") else 0,
                "discapacidad": fam.get("discapacidad"),
                "enfermedad": fam.get("enfermedad"),
                "trabaja": fam.get("trabaja"),
                "ocupacion": fam.get("ocupacion"),
                "ingreso": money_to_float(fam.get("ingreso")),
                "parentesco": fam.get("parentesco"),
            })

        print("DEBUG familiares CON IDS:", familiares)

        # -------------------------
        # 🔍 MAPEAR UBICACIÓN
        # -------------------------
        provincia_id = buscar_id_catalogo(cursor, data.get("datos_provincia"), 18)
        canton_id = buscar_id_catalogo(cursor, data.get("datos_canton"), 19)
        parroquia_id = buscar_id_catalogo(cursor, data.get("datos_parroquias"), 20)
        tipo_parroquia_id = 20 if parroquia_id else None

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
            "datos_internet": si_no(data.get("datos_internet")),
            "datos_pago_internet": data.get("datos_pago_internet"),
            "datos_tv_cable": si_no(data.get("datos_tv_cable")),
            "datos_tv_pago": data.get("datos_tv_pago"),
            "datos_eliminacion_basura": data.get("datos_eliminacion_basura"),
            "datos_lugares_viveres": data.get("datos_lugares_mayor_frecuencia_viveres"),
            "datos_gastos_viveres": data.get("datos_gastos_viveres_alimentacion"),
            "datos_medio_transporte": data.get("datos_medio_transporte"),
            "datos_estado_transporte": data.get("datos_estado_transporte"),
            "datos_terrenos": si_no(data.get("datos_terrenos")),
            "datos_celular": si_no(data.get("datos_celular")),
            "datos_cantidad_celulare": data.get("datos_cantidad_celulare"),
            "datos_plan_celular": si_no(data.get("datos_plan_celular")),
            "datos_observacion": data.get("datos_observacion"),
            "datos_consentimiento": data.get("datos_consentimiento"),

            "familiares": familiares
        }

        print("📨 JSON enviado:", data_api)
        print("DEBUG internet:", data.get("datos_internet"), si_no(data.get("datos_internet")))

        # -------------------------
        # 🌐 ENVIAR A API
        # -------------------------
        try:
            with httpx.Client(timeout=10) as client:
                response = client.post(API_URL, json=data_api)


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
