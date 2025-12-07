from data_base_connection import get_connection

# ID de catálogo para provincias
CAT_PROVINCIAS = 18
CAT_CANTONES = 19
CAT_PARROQUIAS = 20

def get_provincias():
    conn = get_connection() # gets the coneccion from database
    cursor = conn.cursor() # this has all of the methods 
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ?", # executes this query that says return 
        # “I will put a parameter here later.” ?
        (CAT_PROVINCIAS,)  # This is a tuple containing the actual value for the question mark.
    )
    rows = cursor.fetchall() #  Gets all the resulting rows from the query as a list of tuples
    conn.close() # Closes the database connection
    
    lista = []
    for r in rows: # Iterates the rows; each row is a tuple like ("Carchi",)
        lista.append(r[0]) # gets the only column and converts it to a string not a tuple anymore 
    return lista # and appends it to the list


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

def get_parroquias_by_canton_and_tipo(canton_nombre, tipo):
    conn = get_connection()
    cursor = conn.cursor()

    # Convertir tipo a palabras clave
    tipo_palabra = "urbana" if tipo.lower() == "urbano" else "rural"

    cursor.execute(
        """SELECT itc_nombre 
           FROM tbl_item_catalogo
           WHERE id_catalogo = ?
             AND itc_descripcion LIKE ?
             AND itc_descripcion LIKE ?""",
        (CAT_PARROQUIAS,
         f"%{canton_nombre}%",
         f"%{tipo_palabra}%")
    )

    rows = cursor.fetchall()
    conn.close()

    return [r[0] for r in rows]


