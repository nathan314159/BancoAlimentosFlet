import flet as ft

def datos_vivienda_form(page: ft.Page):

    # === TUS CONTROLES ===
    datos_comunidades = ft.TextField(label="Comunidad")
    datos_barrios = ft.TextField(label="Barrio")

    datos_tipo_viviendas = ft.Dropdown(label="Tipo de vivienda", options=[])
    datos_techos = ft.Dropdown(label="Tipo de techo", options=[])
    datos_paredes = ft.Dropdown(label="Tipo de pared", options=[])
    datos_pisos = ft.Dropdown(label="Tipo de piso", options=[])

    datos_cuarto = ft.TextField(label="¿Cuántos cuartos?", value="0", input_filter=ft.NumbersOnlyInputFilter())
    datos_combustibles_cocina = ft.Dropdown(label="Combustible cocina", options=[])
    datos_servicios_higienicos = ft.Dropdown(label="Servicios higiénicos", options=[])

    datos_viviendas = ft.Dropdown(label="Vivienda", options=[])
    datos_pago_vivienda = ft.TextField(label="Pago vivienda", value="0")

    datos_agua = ft.Dropdown(label="Servicio de agua", options=[])
    datos_pago_agua = ft.TextField(label="Pago de agua", value="0")
    datos_pago_luz = ft.TextField(label="Pago de luz", value="0")
    datos_cantidad_luz = ft.TextField(label="Cantidad de luz consumida", value="0")

    # INTERNET
    def toggle_internet(e):
        datos_pago_internet.read_only = (datos_internet.value != "Sí")
        datos_pago_internet.value = "0" if datos_pago_internet.read_only else ""
        page.update()

    datos_internet = ft.Dropdown(
        label="¿Posee servicio de internet?",
        options=[ft.dropdown.Option("Sí"), ft.dropdown.Option("No")],
        on_change=toggle_internet
    )
    datos_pago_internet = ft.TextField(label="Pago internet", value="0", read_only=True)

    # TV
    def toggle_tv(e):
        datos_tv_pago.read_only = (datos_tv_cable.value != "Sí")
        datos_tv_pago.value = "0" if datos_tv_pago.read_only else ""
        page.update()

    datos_tv_cable = ft.Dropdown(
        label="¿Posee TV por cable?",
        options=[ft.dropdown.Option("Sí"), ft.dropdown.Option("No")],
        on_change=toggle_tv
    )
    datos_tv_pago = ft.TextField(label="Pago TV cable", value="0", read_only=True)

    datos_eliminacion_basura = ft.Dropdown(label="Eliminación basura", options=[])
    datos_lugares_viveres = ft.Dropdown(label="Lugares de compra de víveres", options=[])
    datos_gastos_viveres = ft.TextField(label="Gastos en alimentación", value="0")

    # Vehículos
    datos_medio_transporte = ft.Dropdown(label="Tipo de vehículo", options=[])
    datos_estado_transporte = ft.Dropdown(label="Estado del vehículo", options=[])

    tablaVehiculos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Tipo de vehículo")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Acción")),
        ],
        rows=[]
    )

    def agregar_vehiculo(e):
        if datos_medio_transporte.value and datos_estado_transporte.value:
            tablaVehiculos.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(datos_medio_transporte.value)),
                        ft.DataCell(ft.Text(datos_estado_transporte.value)),
                        ft.DataCell(ft.Text("Eliminar")),
                    ]
                )
            )
            page.update()

    btn_agregar_vehiculo = ft.ElevatedButton("Agregar", on_click=agregar_vehiculo)

    # Celulares y terrenos
    def toggle_celular(e):
        datos_cantidad_celulare.read_only = (datos_celular.value != "Sí")
        datos_cantidad_celulare.value = "0" if datos_cantidad_celulare.read_only else ""
        page.update()

    datos_terrenos = ft.Dropdown(label="¿Posee terrenos?", options=[ft.dropdown.Option("Sí"), ft.dropdown.Option("No")])
    datos_celular = ft.Dropdown(label="¿Posee celular?", options=[ft.dropdown.Option("Sí"), ft.dropdown.Option("No")], on_change=toggle_celular)
    datos_cantidad_celulare = ft.TextField(label="Cantidad de celulares", value="0", read_only=True)

    datos_plan_celular = ft.Dropdown(label="¿Tiene plan de celular?", options=[ft.dropdown.Option("Sí"), ft.dropdown.Option("No")])

    datos_observacion = ft.TextField(label="Observaciones", multiline=True)

    datos_resultado_sistema = ft.TextField(label="Resultado automático", value="Pendiente", read_only=True)
    datos_resultado = ft.Dropdown(label="Resultado", options=[
        ft.dropdown.Option("Aprobado"),
        ft.dropdown.Option("No aprobado")
    ])
    criterioMensaje = ft.Text("Criterio", size=18, weight=ft.FontWeight.BOLD)

    def enviar(e):
        page.snack_bar = ft.SnackBar(ft.Text("Datos enviados"))
        page.snack_bar.open = True
        page.update()

    btn_enviar = ft.ElevatedButton("Enviar", on_click=enviar)

    # === AQUÍ LA MAGIA: RETORNAR UN CONTROL ===
    return ft.Column([
        ft.Row([datos_comunidades, datos_barrios]),
        ft.Row([datos_tipo_viviendas, datos_techos, datos_paredes, datos_pisos]),
        ft.Row([datos_cuarto, datos_combustibles_cocina, datos_servicios_higienicos]),
        ft.Row([datos_viviendas, datos_pago_vivienda, datos_agua]),
        ft.Row([datos_pago_agua, datos_pago_luz, datos_cantidad_luz]),
        ft.Row([datos_internet, datos_pago_internet, datos_tv_cable]),
        ft.Row([datos_tv_pago, datos_eliminacion_basura, datos_lugares_viveres]),
        datos_gastos_viveres,
        ft.Text("Vehículos", size=18, weight=ft.FontWeight.BOLD),
        tablaVehiculos,
        ft.Row([datos_medio_transporte, datos_estado_transporte, btn_agregar_vehiculo]),
        ft.Row([datos_terrenos, datos_celular, datos_cantidad_celulare]),
        datos_plan_celular,
        datos_observacion,
        ft.Row([datos_resultado_sistema, datos_resultado, criterioMensaje]),
        btn_enviar
    ], spacing=20)
