from data_base_connection import get_connection

# ID de catálogo para provincias
CAT_PROVINCIAS = 18
CAT_CANTONES = 19
CAT_PARROQUIAS = 20
CAT_ETNIAS = 34
CAT_GENERO = 35
CAT_NIVEL_EDUCACION = 36
CAT_ESTADO_CIVIL = 37

CAT_VIVIENDA = 22
CAT_TECHO = 23
CAT_PARED = 24
CAT_PISO = 25
CAT_COMB_COCINA = 26
CAT_SERV_HIG = 27
CAT_ALOJAMIENTO = 28
CAT_SERV_AGUA = 29
CAT_ELM_BAS = 30
CAT_LUG_FREC_COMPRA = 31
CAT_TIP_VEHICULOS = 32
CAT_EST_TRANSPORTE = 33


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

def get_etnia():
    conn = get_connection() # gets the coneccion from database
    cursor = conn.cursor() # this has all of the methods 
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ?" , # executes this query that says return 
        # “I will put a parameter here later.” ?
        (CAT_ETNIAS,)  # This is a tuple containing the actual value for the question mark. CAT_ETNIAS=34
    )
    rows = cursor.fetchall() #  Gets all the resulting rows from the query as a list of tuples
    conn.close() # Closes the database connection
    
    lista = []
    for r in rows: # Iterates the rows; each row is a tuple like ("Carchi",)
        lista.append(r[0]) # gets the only column and converts it to a string not a tuple anymore 
    return lista # and appends it to the list

def get_genero():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ?" ,
        (CAT_GENERO,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    lista = []
    for r in rows:
        lista.append(r[0])
    return lista 

def get_educacion():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ?" ,
        (CAT_NIVEL_EDUCACION,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    lista = []
    for r in rows:
        lista.append(r[0])
    return lista

def get_estado_civil():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ?" ,
        (CAT_ESTADO_CIVIL,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    lista = []
    for r in rows:
        lista.append(r[0])
    return lista

def get_tipo_viviendas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ?" ,
        (CAT_VIVIENDA,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    lista = []
    for r in rows:
        lista.append(r[0])
    return lista

def get_tipo_techos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ?" ,
        (CAT_TECHO,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    lista = []
    for r in rows:
        lista.append(r[0])
    return lista

def get_tipo_paredes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ?" ,
        (CAT_PARED,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    lista = []
    for r in rows:
        lista.append(r[0])
    return lista

def get_tipo_pisos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ?" ,
        (CAT_PISO,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    lista = []
    for r in rows:
        lista.append(r[0])
    return lista

def get_servicios_higienicos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ?" ,
        (CAT_SERV_HIG,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    lista = []
    for r in rows:
        lista.append(r[0])
    return lista

def get_combustibles_cocina():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ?" ,
        (CAT_COMB_COCINA,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    lista = []
    for r in rows:
        lista.append(r[0])
    return lista

def get_viviendas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ?" ,
        (CAT_ALOJAMIENTO,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    lista = []
    for r in rows:
        lista.append(r[0])
    return lista

def get_viviendas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ?" ,
        (CAT_SERV_AGUA,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    lista = []
    for r in rows:
        lista.append(r[0])
    return lista

def get_liminacion_basura():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ?" ,
        (CAT_ELM_BAS,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    lista = []
    for r in rows:
        lista.append(r[0])
    return lista

def get_lugares_viveres():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ?" ,
        (CAT_LUG_FREC_COMPRA,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    lista = []
    for r in rows:
        lista.append(r[0])
    return lista

def get_estado_transporte():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ?" ,
        (CAT_EST_TRANSPORTE,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    lista = []
    for r in rows:
        lista.append(r[0])
    return lista

def get_medio_transporte():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT itc_nombre FROM tbl_item_catalogo WHERE id_catalogo = ?" ,
        (CAT_TIP_VEHICULOS,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    lista = []
    for r in rows:
        lista.append(r[0])
    return lista


