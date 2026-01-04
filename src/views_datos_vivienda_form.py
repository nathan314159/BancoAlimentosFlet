import flet as ft
from data_base_models import *
from helper import *
from data_base_insert import insert_datos_generales


def datos_vivienda_form(page: ft.Page, get_familiares):

    # ----------------- TÍTULO -----------------
    txt_Datos_vivienda = ft.Text("Datos vivienda", size=18, weight=ft.FontWeight.BOLD)

    # ----------------- DOCUMENTO -----------------
    datos_cedula_voluntario = ft.TextField(
        label="Cédula del voluntario",
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=10,
        width=260,
        disabled=True
    )

    movilidad = ft.Dropdown(
        label="Movilidad", width=260,
        options=[ft.dropdown.Option("Ecuatoriano"), ft.dropdown.Option("Extranjero")]
    )

    def toggle_tipo_documento(e):
        datos_cedula_voluntario.disabled = False
        datos_cedula_voluntario.value = ""
        if movilidad.value == "Ecuatoriano":
            datos_cedula_voluntario.placeholder = "Cédula"
            datos_cedula_voluntario.max_length = 10
        else:
            datos_cedula_voluntario.placeholder = "Pasaporte"
            datos_cedula_voluntario.max_length = 20
        datos_cedula_voluntario.update()

    movilidad.on_change = toggle_tipo_documento

    def validar_documento(e):
        doc = datos_cedula_voluntario.value.strip()
        if movilidad.value == "Ecuatoriano":
            datos_cedula_voluntario.error_text = None if validar_cedula_ecuatoriana(doc) else "Cédula inválida"
        else:
            datos_cedula_voluntario.error_text = None if len(doc) >= 4 else "Documento extranjero demasiado corto"
        datos_cedula_voluntario.update()

    datos_cedula_voluntario.on_blur = validar_documento

    # ----------------- CAMPOS VIVIENDA -----------------
    datos_comunidades = ft.TextField(label="Comunidad", width=260, on_change=solo_letras)
    datos_barrios = ft.TextField(label="Barrio", width=260, on_change=solo_letras)

    datos_tipo_viviendas = ft.Dropdown(label="Tipo de vivienda", width=260)
    load_dropdown_options(datos_tipo_viviendas, get_tipo_viviendas())

    datos_techos = ft.Dropdown(label="Tipo de techo", width=260)
    load_dropdown_options(datos_techos, get_tipo_techos()) 

    datos_paredes = ft.Dropdown(label="Tipo de pared", width=260)
    load_dropdown_options(datos_paredes, get_tipo_paredes()) 

    datos_pisos = ft.Dropdown(label="Tipo de piso", width=260)
    load_dropdown_options(datos_pisos, get_tipo_pisos())

    datos_cuarto = ft.TextField(label="¿Cuántos cuartos?", value="0", input_filter=ft.NumbersOnlyInputFilter())

    datos_combustibles_cocina = ft.Dropdown(label="Combustible cocina", width=260)
    load_dropdown_options(datos_combustibles_cocina, get_combustibles_cocina())

    datos_servicios_higienicos = ft.Dropdown(label="Servicios higiénicos", width=260)
    load_dropdown_options(datos_servicios_higienicos, get_servicios_higienicos())

    datos_viviendas = ft.Dropdown(label="Vivienda", width=260)
    load_dropdown_options(datos_viviendas, get_tipo_alojamiento())

    # ----------------- PAGOS -----------------
    datos_pago_vivienda = money_input("Pago vivienda")
    datos_agua = ft.Dropdown(label="Servicio de agua", width=260)
    load_dropdown_options(datos_agua, get_servicio_agua())
    datos_pago_agua = money_input("Pago agua")
    datos_pago_luz = money_input("Pago de luz")
    datos_cantidad_luz = ft.TextField(label="Cantidad de luz consumida", value="0", input_filter=ft.NumbersOnlyInputFilter())

    # INTERNET
    datos_internet = ft.Dropdown(
        label="¿Posee servicio de internet?", width=260,
        options=[ft.dropdown.Option("Sí"), ft.dropdown.Option("No")]
    )
    datos_pago_internet = money_input("Pago internet", disabled=True)

    def on_internet_change(e):
        if datos_internet.value == "Sí":
            datos_pago_internet.disabled = False
            datos_pago_internet.value = ""
        else:
            datos_pago_internet.disabled = True
            datos_pago_internet.value = ""
        datos_pago_internet.update()

    datos_internet.on_change = on_internet_change

    # TV
    datos_tv_cable = ft.Dropdown(label="¿Posee TV por cable?", width=260, options=[ft.dropdown.Option("Sí"), ft.dropdown.Option("No")])
    datos_tv_pago = money_input("Pago TV cable", disabled=True)

    def on_tv_change(e):
        if datos_tv_cable.value == "Sí":
            datos_tv_pago.disabled = False
            datos_tv_pago.value = ""
        else:
            datos_tv_pago.disabled = True
            datos_tv_pago.value = ""
        datos_tv_pago.update()

    datos_tv_cable.on_change = on_tv_change

    # Otros servicios
    datos_eliminacion_basura = ft.Dropdown(label="Eliminación basura", width=260)
    load_dropdown_options(datos_eliminacion_basura, get_liminacion_basura())
    datos_lugares_viveres = ft.Dropdown(label="Lugares de compra de víveres", width=260)
    load_dropdown_options(datos_lugares_viveres, get_lugares_viveres())
    datos_gastos_viveres = money_input("Gasto en alimentación")

    # VEHÍCULOS
    datos_medio_transporte = ft.Dropdown(label="Tipo de vehículo", width=260)
    load_dropdown_options(datos_medio_transporte, get_medio_transporte())
    datos_estado_transporte = ft.Dropdown(label="Estado del vehículo", width=260)
    load_dropdown_options(datos_estado_transporte, get_estado_transporte())

    tablaVehiculos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Tipo de vehículo")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Acción")),
        ],
        rows=[]
    )

    def eliminar_fila(row):
        tablaVehiculos.rows.remove(row)
        tablaVehiculos.update()

    def agregar_vehiculo(e):
        if datos_medio_transporte.value and datos_estado_transporte.value:
            row = ft.DataRow(cells=[
                ft.DataCell(ft.Text(datos_medio_transporte.value)),
                ft.DataCell(ft.Text(datos_estado_transporte.value)),
                ft.DataCell(ft.Text("")),  # placeholder
            ])
            btn_delete = ft.IconButton(icon=ft.Icons.DELETE, icon_color="red", on_click=lambda e: eliminar_fila(row))
            row.cells[2] = ft.DataCell(btn_delete)
            tablaVehiculos.rows.append(row)
            tablaVehiculos.update()

    btn_agregar_vehiculo = ft.ElevatedButton("Agregar", on_click=agregar_vehiculo)

    # CELULARES Y TERRENOS
    datos_terrenos = ft.Dropdown(label="¿Posee terrenos?", options=[ft.dropdown.Option("Sí"), ft.dropdown.Option("No")], width=260)
    datos_celular = ft.Dropdown(label="¿Posee celular?", options=[ft.dropdown.Option("Sí"), ft.dropdown.Option("No")], width=260)
    datos_cantidad_celulare = ft.TextField(label="Cantidad de celulares", value="0", read_only=True, width=260)

    def toggle_celular(e):
        datos_cantidad_celulare.read_only = (datos_celular.value != "Sí")
        datos_cantidad_celulare.value = "0" if datos_cantidad_celulare.read_only else ""
        datos_cantidad_celulare.update()

    datos_celular.on_change = toggle_celular

    datos_plan_celular = ft.Dropdown(label="¿Tiene plan de celular?", options=[ft.dropdown.Option("Sí"), ft.dropdown.Option("No")], width=260)

    # OBSERVACIONES Y RESULTADOS
    datos_observacion = ft.TextField(label="Observaciones", multiline=True, min_lines=5, max_lines=10, expand=True)
    datos_resultado_sistema = ft.TextField(label="Resultado automático", value="Pendiente", read_only=True)
    datos_resultado = ft.Dropdown(label="Resultado", options=[ft.dropdown.Option("Aprobado"), ft.dropdown.Option("No aprobado")], width=260)
    criterioMensaje = ft.Text("Criterio", size=18, weight=ft.FontWeight.BOLD)
    
    # ----------------- FUNCIONES -----------------
    def obtener_datos_vivienda():
        return {
            "datos_cedula_voluntario": datos_cedula_voluntario.value,
            "datos_comunidades": datos_comunidades.value,
            "datos_barrios": datos_barrios.value,
            "datos_tipo_viviendas": datos_tipo_viviendas.value,
            "datos_techos": datos_techos.value,
            "datos_paredes": datos_paredes.value,
            "datos_pisos": datos_pisos.value,
            "datos_cuarto": datos_cuarto.value,
            "datos_combustibles_cocina": datos_combustibles_cocina.value,
            "datos_servicios_higienicos": datos_servicios_higienicos.value,
            "datos_viviendas": datos_viviendas.value,
            "datos_pago_vivienda": datos_pago_vivienda.value,
            "datos_agua": datos_agua.value,
            "datos_pago_agua": datos_pago_agua.value,
            "datos_pago_luz": datos_pago_luz.value,
            "datos_cantidad_luz": datos_cantidad_luz.value,
            "datos_internet": datos_internet.value,
            "datos_pago_internet": datos_pago_internet.value,
            "datos_tv_cable": datos_tv_cable.value,
            "datos_tv_pago": datos_tv_pago.value,
            "datos_eliminacion_basura": datos_eliminacion_basura.value,
            "datos_lugares_viveres": datos_lugares_viveres.value,
            "datos_gastos_viveres": datos_gastos_viveres.value,
            "datos_terrenos": datos_terrenos.value,
            "datos_celular": datos_celular.value,
            "datos_cantidad_celulare": datos_cantidad_celulare.value,
            "datos_plan_celular": datos_plan_celular.value,
            "datos_observacion": datos_observacion.value,
            "datos_resultado": datos_resultado.value,
            "datos_resultado_sistema": datos_resultado_sistema.value,
        }

    def validar_vivienda():
        campos_obligatorios = [
            datos_comunidades, datos_barrios, datos_tipo_viviendas,
            datos_techos, datos_paredes, datos_pisos, datos_viviendas,
            datos_agua, datos_eliminacion_basura
        ]
        valido = True
        for campo in campos_obligatorios:
            if not campo.value:
                campo.error_text = "Campo obligatorio"
                valido = False
            else:
                campo.error_text = None
            campo.update()
        return valido

    # ----------------- BOTÓN CALCULAR RESULTADO -----------------
    def calcular_resultado(e):
        # Obtener familiares de la UI
        familiares = get_familiares()  # esta función debe venir de tu familiares_view

        # Construir tablaParentesco
        tabla_parentesco = [{"ingreso_mensual": safe_float(f.get("ingreso", 0))} for f in familiares]

        # Recolectar datos de vehículos
        tabla_vehiculos_data = [{"datos_estado_transporte": row.cells[1].content.value} for row in tablaVehiculos.rows]

        # Llamar a evaluar_resultado
        resultado_sistema, mensaje_criterio = evaluar_resultado(
            tabla_parentesco=tabla_parentesco,
            tabla_vehiculos=tabla_vehiculos_data,
            datos_pago_vivienda=datos_pago_vivienda.value,
            datos_pago_agua=datos_pago_agua.value,
            datos_pago_luz=datos_pago_luz.value,
            datos_pago_internet=datos_pago_internet.value,
            datos_tv_pago=datos_tv_pago.value,
            datos_gastos_viveres_alimentacion=datos_gastos_viveres.value,
            id_datos_generales=1  # reemplazar por el ID real al guardar
        )

        # Actualizar UI
        datos_resultado_sistema.value = resultado_sistema
        datos_resultado_sistema.bgcolor = ft.Colors.GREEN_100 if resultado_sistema == "Aprobado" else ft.Colors.RED_100
        datos_resultado_sistema.update()

        criterioMensaje.value = mensaje_criterio
        criterioMensaje.update()

    btn_calcular = ft.ElevatedButton("Calcular Resultado", on_click=calcular_resultado)

    # ----------------- LAYOUT -----------------
    contenido = ft.Column([
        ft.Row([txt_Datos_vivienda], wrap=True),
        ft.Row([datos_comunidades, datos_barrios], wrap=True),
        ft.Row([datos_tipo_viviendas, datos_techos, datos_paredes, datos_pisos], wrap=True),
        ft.Row([datos_cuarto, datos_combustibles_cocina, datos_servicios_higienicos], wrap=True),
        ft.Row([datos_viviendas, datos_pago_vivienda, datos_agua], wrap=True),
        ft.Row([datos_pago_agua, datos_pago_luz, datos_cantidad_luz], wrap=True),
        ft.Row([datos_internet, datos_pago_internet], wrap=True),
        ft.Row([datos_tv_cable, datos_tv_pago], wrap=True),
        ft.Row([datos_eliminacion_basura, datos_lugares_viveres], wrap=True),
        datos_gastos_viveres,
        ft.Text("Vehículos", size=18, weight=ft.FontWeight.BOLD),
        tablaVehiculos,
        ft.Row([datos_medio_transporte, datos_estado_transporte, btn_agregar_vehiculo], wrap=True),
        ft.Row([datos_terrenos, datos_celular, datos_cantidad_celulare], wrap=True),
        datos_plan_celular,
        datos_observacion,
        ft.Row([datos_resultado_sistema, datos_resultado, criterioMensaje], wrap=True),
        ft.Row([movilidad, datos_cedula_voluntario], wrap=True),
        btn_calcular
    ], spacing=20)

    return contenido, obtener_datos_vivienda, validar_vivienda, tablaVehiculos, datos_resultado_sistema, criterioMensaje


