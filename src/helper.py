# import flet as ft
import os
import sqlite3
from datetime import *
# def money_input(label="Monto", value="", disabled=False, width=260 ):
#     def validate_numeric(e):
#         if field.disabled:   # 👈 CLAVE
#             return
        
#         txt = field.value.replace(",", "").replace(" ", "")

#         # Allow empty while typing
#         if txt == "":
#             return
        
#         # Allow digits and ONE decimal point
#         if not txt.replace(".", "", 1).isdigit():
#             field.value = prev_value[0]  # restore last valid value
#         else:
#             prev_value[0] = field.value  # keep latest valid

#         e.page.update()

#     def format_on_blur(e):
#         txt = field.value.replace(",", "").replace(" ", "")
#         if txt == "":
#             field.value = ""
#         else:
#             number = float(txt)
#             field.value = f"{number:,.2f}"
#         e.page.update()

#     prev_value = [""]  # store last valid input

#     field = ft.TextField(
#         label=label,
#         value=value,
#         on_change=validate_numeric,   # no formatting while typing
#         on_blur=format_on_blur,       # format only when leaving the field
#         keyboard_type=ft.KeyboardType.NUMBER,
#         disabled=disabled,
#         width=width
#     )

#     return field

# def load_dropdown_options(control, items):
#     control.options = [ft.dropdown.Option(i) for i in items]

# def solo_letras(e):
#     control = e.control
#     if not control.value.replace(" ", "").isalpha():
#         control.error_text = "Solo letras"
#     else:
#         control.error_text = None
#     control.update()

# def solo_numeros(e):
#     control = e.control
#     if not control.value.isdigit():
#         control.error_text = "Solo números positivos"
#     else:
#         control.error_text = None
#     control.update()

# def validar_cedula_ecuatoriana(cedula: str) -> bool:
#     cedula = cedula.strip()
#     if not cedula.isdigit() or len(cedula) != 10:
#         return False

#     provincia = int(cedula[:2])
#     tercer_digito = int(cedula[2])

#     if provincia < 1 or (provincia > 24 and provincia != 30):
#         return False
#     if tercer_digito >= 6:
#         return False

#     coef = [2, 1, 2, 1, 2, 1, 2, 1, 2]
#     suma = 0

#     for i in range(9):
#         val = int(cedula[i]) * coef[i]
#         if val >= 10:
#             val -= 9
#         suma += val

#     verificador = 10 - (suma % 10 if suma % 10 != 0 else 10)
#     return verificador == int(cedula[9])

import flet as ft

# =========================
# MONEY INPUT
# =========================
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


# =========================
# DROPDOWNS CON ID REAL
# =========================
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

# =========================
# CONVERSORES
# =========================
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

def get_nombre_catalogo(cursor, id_item):
    """
    Retorna el nombre (itc_nombre) de un item del catálogo según su ID.
    """
    if not id_item:
        return None

    cursor.execute("""
        SELECT itc_nombre
        FROM tbl_item_catalogo
        WHERE id_item = ?
          AND itc_estado = 1
        LIMIT 1
    """, (id_item,))

    row = cursor.fetchone()
    return row[0] if row else None

def get_nombre_catalogo(cursor, id_item):
    """
    Retorna el nombre (itc_nombre) de un item del catálogo según su ID.
    """
    if not id_item:
        return None

    cursor.execute("""
        SELECT itc_descripcion
        FROM tbl_item_catalogo
        WHERE id_item = ?
          AND itc_estado = 1
        LIMIT 1
    """, (id_item,))

    row = cursor.fetchone()
    return row[0] if row else None

def get_nombre_y_tipo_parroquia(cursor, id_item):
    """
    Retorna el nombre y tipo (urbano/rural) de un item del catálogo según su ID.
    """
    if not id_item:
        return None, None

    cursor.execute("""
        SELECT itc_descripcion,
               CASE 
                   WHEN itc_descripcion LIKE '%urbana%' THEN 'urbano'
                   WHEN itc_descripcion LIKE '%rural%' THEN 'rural'
                   ELSE 'desconocido'
               END AS tipo_parroquia
        FROM tbl_item_catalogo
        WHERE id_item = ?
          AND itc_estado = 1
        LIMIT 1
    """, (id_item,))

    row = cursor.fetchone()
    if row:
        descripcion, tipo_parroquia = row
        return descripcion, tipo_parroquia
    return None, None




