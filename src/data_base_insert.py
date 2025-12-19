from data_base_connection import get_connection

def obtener_transportes(tablaVehiculos):
    medios = []
    estados = []

    for row in tablaVehiculos.rows:
        medios.append(row.cells[0].content.value)
        estados.append(row.cells[1].content.value)

    return "/".join(medios), "/".join(estados)

def insert_datos_generales(data: dict, tablaVehiculos):
    conn = get_connection()
    cursor = conn.cursor()

    # Convertir DataTable a TEXT
    medios, estados = obtener_transportes(tablaVehiculos)
    print("CEDULA:", data["datos_cedula_voluntario"])
    print("MEDIOS:", medios)
    print("ESTADOS:", estados)

    cursor.execute("""
        INSERT INTO tbl_datos_generales (
            datos_cedula_voluntario,
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
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        data["datos_cedula_voluntario"],
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
        medios,        # ← AQUÍ
        estados,       # ← AQUÍ
        data["datos_terrenos"],
        data["datos_celular"],
        data["datos_cantidad_celulare"],
        data["datos_plan_celular"],
        data["datos_observacion"],
        data["datos_resultado"],
        data["datos_resultado_sistema"]
    ))

    conn.commit()
    print("ROWCOUNT:", cursor.rowcount)
    cursor.execute("SELECT COUNT(*) FROM tbl_datos_generales")
    print("TOTAL REGISTROS:", cursor.fetchone()[0])

    last_id = cursor.lastrowid
    conn.close()
    return last_id
