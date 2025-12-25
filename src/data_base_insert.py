import sqlite3
from data_base_connection import DB_PATH, get_connection

def obtener_transportes(tablaVehiculos):
    medios = []
    estados = []

    for row in tablaVehiculos.rows:
        medios.append(row.cells[0].content.value)
        estados.append(row.cells[1].content.value)

    return "/".join(medios), "/".join(estados)

def insert_datos_generales(data: dict, tablaVehiculos):
    print("Provincia que voy a insertar:", data.get("provincia"))
    
    conn = get_connection()
    cursor = conn.cursor()

    try:
        medios, estados = obtener_transportes(tablaVehiculos)

        cursor.execute("""
            INSERT INTO tbl_datos_generales_PRUEBA (
                uuid,
                datos_cedula_voluntario,
                datos_parentesco_id,
                datos_provincia,
                datos_canton,
                datos_tipo_parroquias,
                datos_parroquias,
                datos_comunidades,
                datos_barrios,
                datos_tipo_viviendas,
                
                datos_techos,
                datos_paredes,
                datos_pisos,
                datos_cuarto,
                datos_combustibles_cocina,
                datos_servicios_higienicos,
                datos_viviendas,
                datos_pago_vivienda,
                datos_agua,
                datos_pago_agua,
                
                datos_pago_luz,                
                datos_cantidad_luz,
                datos_internet,
                datos_pago_internet,
                datos_tv_cable,
                datos_tv_pago,
                datos_eliminacion_basura,
                datos_lugares_mayor_frecuencia_viveres,
                datos_gastos_viveres_alimentacion,
                datos_medio_transporte,
                
                datos_estado_transporte,
                datos_terrenos,
                datos_celular,
                datos_cantidad_celulare,
                datos_plan_celular,
                datos_observacion,
                datos_resultado,
                datos_resultado_sistema
            ) VALUES (?,?,?,?,?,?,?,?,?,?,  ?,?,?,?,?,?,?,?,?,?,  ?,?,?,?,?,?,?,?,?,?,  ?,?,?,?,?,?,?,?)
        """, (
            data["uuid"],
            data["datos_cedula_voluntario"],
            None,
            data["provincia"],
            data["canton"],
            data["tipo_parroquia"],
            data["parroquia"],
            data["datos_comunidades"],
            data["datos_barrios"],
            data["datos_tipo_viviendas"],
            data["datos_techos"],
            data["datos_paredes"],
            data["datos_pisos"],
            data["datos_cuarto"],
            data["datos_combustibles_cocina"],
            data["datos_servicios_higienicos"],
            data["datos_viviendas"],
            data["datos_pago_vivienda"],
            data["datos_agua"],
            data["datos_pago_agua"],
            data["datos_pago_luz"],
            data["datos_cantidad_luz"],
            data["datos_internet"],
            data["datos_pago_internet"],
            data["datos_tv_cable"],
            data["datos_tv_pago"],
            data["datos_eliminacion_basura"],
            data["datos_lugares_viveres"],
            data["datos_gastos_viveres"],
            medios,
            estados,
            data["datos_terrenos"],
            data["datos_celular"],
            data["datos_cantidad_celulare"],
            data["datos_plan_celular"],
            data["datos_observacion"],
            data["datos_resultado"],
            data["datos_resultado_sistema"]
        ))

        id_general = cursor.lastrowid
        print("DEBUG familiares al guardar en SQLite:", data["familiares"])

        primer_parentesco = insert_parentescos(
            cursor,
            data["familiares"],
            id_general
        )

        if primer_parentesco:
            cursor.execute("""
                UPDATE tbl_datos_generales_PRUEBA
                SET datos_parentesco_id = ?
                WHERE id_datos_generales = ?
            """, (primer_parentesco, id_general))

        conn.commit()
        return id_general

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()

def insert_parentescos(cursor, familiares, id_datos_generales):
    """
    Inserta los familiares en tbl_datos_parentesco
    y devuelve el ID del PRIMER parentesco (para datos_parentesco_id)
    """

    primer_parentesco_id = None

    for i, fam in enumerate(familiares):
        cursor.execute("""
            INSERT INTO tbl_datos_parentesco (
                datos_parentesco_nombres,
                datos_parentesco_apellidos,
                datos_parentesco_documento,
                datos_parentesco_celular_telf,
                datos_parentesco_etnia,
                datos_parentesco_genero,
                datos_parentesco_nivel_educacion,
                datos_parentesco_fecha_de_nacimiento,
                datos_parentesco_edad,
                datos_parentesco_estado_civil,
                
                datos_parentesco_discapacidad,
                datos_parentesco_enfermedad_catastrofica,
                datos_parentesco_trabaja,
                datos_parentesco_ocupacion,
                datos_parentesco_ingreso_mensual,
                datos_parentesco_parentesco
            ) VALUES (?,?,?,?,?,?,?,?,?,?,  ?,?,?,?,?,?)
        """, (
            fam.get("nombres"),
            fam.get("apellidos"),
            fam.get("documento"),
            fam.get("telefono"),
            fam.get("etnia"),
            fam.get("genero"),
            fam.get("nivel_educacion"),
            fam.get("fecha_nacimiento"),
            fam.get("edad"),
            fam.get("estado_civil"),
            fam.get("discapacidad"),
            fam.get("enfermedad"),
            fam.get("trabaja"),
            fam.get("ocupacion"),
            fam.get("ingreso"),
            fam.get("parentesco"),
        ))

        id_parentesco = cursor.lastrowid

        # Guardar el PRIMER parentesco (como en PHP)
        if i == 0:
            primer_parentesco_id = id_parentesco

        # 🔗 Tabla relación (si la usas)
        cursor.execute("""
            INSERT INTO tbl_datos_generales_parentesco (
                id_datos_generales,
                id_datos_parentescos
            ) VALUES (?, ?)
        """, (id_datos_generales, id_parentesco))

    return primer_parentesco_id




