# import flet as ft
import os
import sqlite3
from datetime import *
import flet as ft
import socket
import httpx

def money_input(label="Monto", value="", disabled=False, width=260):
    def validate_numeric(e):
        if field.disabled:
            return

        txt = field.value.replace(",", "").replace(" ", "")

        if txt == "":
            return

        if not txt.replace(".", "", 1).isdigit():
            field.value = prev_value[0]
        else:
            prev_value[0] = field.value

        e.page.update()

    def format_on_blur(e):
        txt = field.value.replace(",", "").replace(" ", "")
        if txt == "":
            field.value = ""
        else:
            number = float(txt)
            field.value = f"{number:,.2f}"
        e.page.update()

    prev_value = [""]

    field = ft.TextField(
        label=label,
        value=value,
        on_change=validate_numeric,
        on_blur=format_on_blur,
        keyboard_type=ft.KeyboardType.NUMBER,
        disabled=disabled,
        width=width
    )

    return field

def load_dropdown_options(control, items):
    """
    items puede ser:
      - Lista de diccionarios: [{ "id": 1, "nombre": "Casa" }]
      - Lista simple de strings: ["Casa", "Departamento"]
    """
    if items and isinstance(items[0], dict):
        control.options = [
            ft.dropdown.Option(
                key=str(i["id"]),    # ahora usamos 'key' en lugar de 'value'
                text=i["nombre"]
            )
            for i in items
        ]
    else:
        control.options = [
            ft.dropdown.Option(
                key=str(i),          # 'key' en lugar de 'value'
                text=str(i)
            )
            for i in items
        ]



def si_no(value):
    return 1 if value == "Sí" else 0


def money_to_int(value):
    if not value:
        return 0
    return int(float(value.replace(",", "")))


def safe_int(value):
    try:
        return int(value)
    except:
        return 0


# =========================
# VALIDACIONES
# =========================
def solo_letras(e):
    control = e.control
    if not control.value.replace(" ", "").isalpha():
        control.error_text = "Solo letras"
    else:
        control.error_text = None
    control.update()


def validar_cedula_ecuatoriana(cedula: str) -> bool:
    cedula = cedula.strip()
    if not cedula.isdigit() or len(cedula) != 10:
        return False

    provincia = int(cedula[:2])
    tercer_digito = int(cedula[2])

    if provincia < 1 or (provincia > 24 and provincia != 30):
        return False
    if tercer_digito >= 6:
        return False

    coef = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = 0

    for i in range(9):
        val = int(cedula[i]) * coef[i]
        if val >= 10:
            val -= 9
        suma += val

    verificador = 10 - (suma % 10 if suma % 10 != 0 else 10)
    return verificador == int(cedula[9])



# # Directorio del archivo connection.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta correcta de la BD
DB_PATH = os.path.join(BASE_DIR, "app.db")

def get_item_ids_flexible(nombre_item: str, id_catalogo: int, db_path=DB_PATH) -> list[int]:
    """
    Devuelve una lista de id_item que contengan el nombre_item en itc_nombre o itc_descripcion.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id_item
            FROM tbl_item_catalogo
            WHERE (LOWER(itc_nombre) LIKE LOWER(?) OR LOWER(itc_descripcion) LIKE LOWER(?))
              AND id_catalogo = ?
              AND itc_estado = 1
        """, (f"%{nombre_item.strip()}%", f"%{nombre_item.strip()}%", id_catalogo))
        
        results = cursor.fetchall()
        return [row[0] for row in results]
    finally:
        conn.close()


def money_to_float(value):
    if value is None or value == "":
        return 0.0
    try:
        return float(str(value).replace(",", ""))
    except ValueError:
        return 0.0



def convertir_fecha(fecha_str):
    try:
        return datetime.strptime(fecha_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except Exception as e:
        print("❌ Fecha inválida:", fecha_str, e)
        return None



def hay_internet(timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except Exception:
        return False

import httpx

def backend_disponible(url, timeout=3):
    try:
        r = httpx.get(url, timeout=timeout)
        return True
    except httpx.ConnectError:
        return False
    except Exception as e:
        print("Backend check error:", e)
        return False


def escribir_estado_sync(pendientes):
    with open("estado_sync.txt", "w", encoding="utf-8") as f:
        f.write(f"⏳ Encuestas pendientes: {pendientes}")
