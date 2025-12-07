from data_base_connection import get_connection

# ID de catálogo para provincias
CAT_PROVINCIAS = 18
CAT_CANTONES = 19
CAT_PARROQUIAS = 20

def get_provincias():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ?", 
        (CAT_PROVINCIAS,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

def get_cantones_by_provincia(provincia_nombre):
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Obtener el código de la provincia
    cursor.execute(
        "SELECT itc_codigo FROM tbl_item_catalogo WHERE itc_nombre = ? AND id_catalogo = ?",
        (provincia_nombre, CAT_PROVINCIAS)
    )
    res = cursor.fetchone()
    if not res:
        conn.close()
        return []
    provincia_codigo = res[0]

    # 2. Listar cantones de esa provincia
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ? AND itc_descripcion LIKE ?",
        (CAT_CANTONES, f"%{provincia_codigo}%")
    )
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

# def get_parroquias_by_canton_and_tipo(canton_nombre, tipo):
#     conn = get_connection()
#     cursor = conn.cursor()

#     # 1. Obtener código del cantón
#     cursor.execute(
#         "SELECT itc_codigo FROM tbl_item_catalogo WHERE itc_nombre = ? AND id_catalogo = ?",
#         (canton_nombre, CAT_CANTONES)
#     )
#     res = cursor.fetchone()
#     if not res:
#         conn.close()
#         return []
#     canton_codigo = res[0]

#     # 2. Filtro por TIPO usando LIKE
#     tipo_palabra = "urbana" if tipo.lower() == "urbano" else "rural"

#     cursor.execute(
#         """SELECT itc_nombre 
#            FROM tbl_item_catalogo 
#            WHERE id_catalogo = ? 
#            AND itc_codigo LIKE ?
#            AND itc_descripcion LIKE ?""",
#         (CAT_PARROQUIAS, f"%{canton_codigo}%", f"%{tipo_palabra}%")
#     )

#     rows = cursor.fetchall()
#     conn.close()

#     return [r[0] for r in rows]
