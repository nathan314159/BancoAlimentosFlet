from data_base_models import get_etnia, get_genero, get_educacion, get_estado_civil
from helper import *
import flet as ft

def familiares_view(page: ft.Page):

    page.overlay.clear()

    # -------- TABLA PRINCIPAL --------
    tabla_familiares = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombres")),
            ft.DataColumn(ft.Text("Apellidos")),
            ft.DataColumn(ft.Text("Documento")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Etnia")),
            ft.DataColumn(ft.Text("Género")),
            ft.DataColumn(ft.Text("Nivel Educación")),
            ft.DataColumn(ft.Text("Fecha Nac.")),
            ft.DataColumn(ft.Text("Edad")),
            ft.DataColumn(ft.Text("Estado Civil")),
            ft.DataColumn(ft.Text("Discapacidad")),
            ft.DataColumn(ft.Text("Enf. Catastrófica")),
            ft.DataColumn(ft.Text("Trabaja")),
            ft.DataColumn(ft.Text("Ocupación")),
            ft.DataColumn(ft.Text("Ingreso")),
            ft.DataColumn(ft.Text("Parentesco")),
            ft.DataColumn(ft.Text("Acción")),
        ],
        rows=[]
    )

    # -------- CAMPOS --------
    nombres = ft.TextField(label="Nombres", width=260, on_change=solo_letras)
    apellidos = ft.TextField(label="Apellidos", width=260, on_change=solo_letras)
    movilidad = ft.Dropdown(
        label="Movilidad", width=260,
        options=[
            ft.dropdown.Option("Ecuatoriano"),
            ft.dropdown.Option("Extranjero")
        ]
    )
    documento = ft.TextField(label="Documento", width=260, disabled=True)
    celular = ft.TextField(label="Celular", width=260, input_filter=ft.NumbersOnlyInputFilter())
    etnia = ft.Dropdown(label="Etnia", width=260)
    genero = ft.Dropdown(label="Género", width=260)
    nivel_educacion = ft.Dropdown(label="Nivel Educación", width=260)
    estado_civil = ft.Dropdown(label="Estado Civil", width=260)

    # -------- FECHA NACIMIENTO --------
    fecha_nacimiento = ft.TextField(label="Fecha Nacimiento", width=260, read_only=True)

    # date_picker = ft.DatePicker(
    #     on_change=lambda e: (
    #         setattr(fecha_nacimiento, "value", e.control.value),
    #         fecha_nacimiento.update()
    #     )
    # )
    # page.overlay.append(date_picker)
    
    def on_date_selected(e):
        if e.control.value:
            fecha_nacimiento.value = e.control.value.strftime("%d/%m/%Y")
            fecha_nacimiento.update()

    
    date_picker = ft.DatePicker(
        on_change=lambda e: on_date_selected(e)
    )

    page.overlay.append(date_picker)

    def open_calendar():
        date_picker.open = True
        page.update()

    btn_fecha = ft.IconButton(
        icon=ft.Icons.CALENDAR_MONTH,
        tooltip="Seleccionar fecha",
        on_click=lambda e: open_calendar()
    )


    edad = ft.TextField(label="Edad", width=260, input_filter=ft.NumbersOnlyInputFilter())

    # -------- DISCAPACIDAD --------
    def on_discapacidad_change(e):
        enfermedad.disabled = (discapacidad.value == "No")
        if enfermedad.disabled:
            enfermedad.value = ""
        enfermedad.update()

    discapacidad = ft.Dropdown(
        label="Discapacidad",
        width=260,
        options=[ft.dropdown.Option("Sí"), ft.dropdown.Option("No")],
        on_change=on_discapacidad_change,
    )

    enfermedad = ft.TextField(
        label="Enfermedad Catastrófica",
        width=260,
        value="Ninguna",
        disabled=True
    )

    # -------- TRABAJA --------
    def on_trabaja_change(e):
        ocupacion.disabled = (trabaja.value == "No")
        if ocupacion.disabled:
            ocupacion.value = ""
        ocupacion.update()

    trabaja = ft.Dropdown(
        label="¿Trabaja?",
        width=260,
        options=[ft.dropdown.Option("Sí"), ft.dropdown.Option("No")],
        on_change=on_trabaja_change
    )

    ocupacion = ft.TextField(label="Ocupación", width=260, disabled=True, on_change=solo_letras)
    ingreso = ft.TextField(label="Ingreso Mensual", width=260)
    ingreso = money_input("Ingreso Mensual")
    parentesco = ft.TextField(label="Parentesco", width=260, on_change=solo_letras)

    # -------- CARGAR BD --------
    etnia.options = [ft.dropdown.Option(i) for i in get_etnia()]
    genero.options = [ft.dropdown.Option(i) for i in get_genero()]
    nivel_educacion.options = [ft.dropdown.Option(i) for i in get_educacion()]
    estado_civil.options = [ft.dropdown.Option(i) for i in get_estado_civil()]
    
    # -------- MOVILIDAD --------
    def toggle_tipo_documento(e):
        documento.disabled = False
        documento.value = ""

        if movilidad.value == "Ecuatoriano":
            documento.placeholder = "Cédula"
            documento.max_length = 10
        else:
            documento.placeholder = "Pasaporte"
            documento.max_length = 20

        documento.update()

    movilidad.on_change = toggle_tipo_documento

    # -------- VALIDAR DOCUMENTO --------
    def validar_documento(e):
        doc = documento.value.strip()

        if movilidad.value == "Ecuatoriano":
            documento.error_text = None if validar_cedula_ecuatoriana(doc) else "Cédula inválida"
        else:
            documento.error_text = None if len(doc) >= 4 else "Documento extranjero demasiado corto"

        documento.update()

    documento.on_blur = validar_documento

    # -------- AGREGAR A LA TABLA --------
    def eliminar_fila(row):
        tabla_familiares.rows.remove(row)
        page.update()

    def validar_campos_obligatorios(campos):
        errores = False

        for campo, mensaje in campos:
            valor = campo.value

            # ---- Caso 1: TextField (string) ----
            if isinstance(valor, str):
                if valor.strip() == "":
                    campo.error_text = mensaje
                    errores = True
                else:
                    campo.error_text = None

            # ---- Caso 2: Dropdown (elige opción) ----
            elif isinstance(campo, ft.Dropdown):
                if campo.value is None or campo.value == "":
                    campo.error_text = mensaje
                    errores = True
                else:
                    campo.error_text = None

            # ---- Caso 3: DatePicker (usa string en tu TextField fecha_nacimiento) ----
            elif isinstance(campo, ft.TextField) and campo == fecha_nacimiento:
                if campo.value is None or campo.value == "":
                    campo.error_text = mensaje
                    errores = True
                else:
                    campo.error_text = None

            campo.update()

        return errores

    def add_familiar(e):

        campos_obligatorios = [
            (nombres, "Ingrese un nombre"),
            (apellidos, "Ingrese un apellido"),
            (documento, "Ingrese un documento"),
            (celular, "Ingrese un celular"),
            (genero, "Seleccione un género"),
            (nivel_educacion, "Seleccione nivel de educación"),
            (fecha_nacimiento, "Ingrese fecha nacimiento"),
            (edad, "Ingrese edad"),
            (estado_civil, "Seleccione estado civil"),
            (ingreso, "Ingrese ingreso mensual"),
            (parentesco, "Ingrese parentesco"),
        ]

        # Validación general
        if validar_campos_obligatorios(campos_obligatorios):
            return

        # Validar enfermedad si discapacidad = Sí
        if discapacidad.value == "Sí" and enfermedad.value.strip() == "":
            enfermedad.error_text = "Ingrese enfermedad"
            enfermedad.update()
            return
        else:
            enfermedad.error_text = None
            enfermedad.update()

        # Validar ocupación si trabaja = Sí
        if trabaja.value == "Sí" and ocupacion.value.strip() == "":
            ocupacion.error_text = "Ingrese ocupación"
            ocupacion.update()
            return
        else:
            ocupacion.error_text = None
            ocupacion.update()



        row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(nombres.value)),
                ft.DataCell(ft.Text(apellidos.value)),
                ft.DataCell(ft.Text(documento.value)),
                ft.DataCell(ft.Text(celular.value)),
                ft.DataCell(ft.Text(etnia.value)),
                ft.DataCell(ft.Text(genero.value)),
                ft.DataCell(ft.Text(nivel_educacion.value)),
                ft.DataCell(ft.Text(fecha_nacimiento.value)),
                ft.DataCell(ft.Text(edad.value)),
                ft.DataCell(ft.Text(estado_civil.value)),
                ft.DataCell(ft.Text(discapacidad.value)),
                ft.DataCell(ft.Text(enfermedad.value)),
                ft.DataCell(ft.Text(trabaja.value)),
                ft.DataCell(ft.Text(ocupacion.value)),
                ft.DataCell(ft.Text(ingreso.value)),
                ft.DataCell(ft.Text(parentesco.value)),
                ft.DataCell(
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color="red",
                        on_click=lambda _: eliminar_fila(row)
                    )
                ),
            ]
        )

        tabla_familiares.rows.append(row)
                # ---- LIMPIAR CAMPOS ----
        nombres.value = ""
        apellidos.value = ""
        movilidad.value = None
        documento.value = ""
        celular.value = ""
        etnia.value = None
        genero.value = None
        nivel_educacion.value = None
        fecha_nacimiento.value = ""
        edad.value = ""
        estado_civil.value = None
        discapacidad.value = None
        enfermedad.value = ""
        trabaja.value = None
        ocupacion.value = ""
        ingreso.value = ""
        parentesco.value = ""

        # Reset de campos dependientes
        documento.disabled = True
        enfermedad.disabled = True
        ocupacion.disabled = True

        # Remover errores visuales
        for c in [
            nombres, apellidos, documento, celular, etnia, genero,
            nivel_educacion, fecha_nacimiento, edad, estado_civil,
            discapacidad, enfermedad, trabaja, ocupacion, ingreso, parentesco
        ]:
            c.error_text = None
            c.update()



        page.update()

    def obtener_familiares():
        familiares = []

        for row in tabla_familiares.rows:
            familiares.append({
                "nombres": row.cells[0].content.value,
                "apellidos": row.cells[1].content.value,
                "documento": row.cells[2].content.value,
                "telefono": row.cells[3].content.value,
                "etnia": row.cells[4].content.value,
                "genero": row.cells[5].content.value,
                "nivel_educacion": row.cells[6].content.value,
                "fecha_nacimiento": row.cells[7].content.value,
                "edad": row.cells[8].content.value,
                "estado_civil": row.cells[9].content.value,
                "discapacidad": row.cells[10].content.value,
                "enfermedad": row.cells[11].content.value,
                "trabaja": row.cells[12].content.value,
                "ocupacion": row.cells[13].content.value,
                "ingreso": row.cells[14].content.value,
                "parentesco": row.cells[15].content.value,
            })

        return familiares


    # -------- WRAPPER CON SCROLL --------
    tabla_scroll = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[tabla_familiares],
                    scroll=ft.ScrollMode.AUTO  # horizontal
                )
            ],
            scroll=ft.ScrollMode.AUTO          # vertical
        ),
        width=1000,
        height=350,
        border=ft.border.all(1, "gray"),
        padding=10
    )

    # -------- LAYOUT FINAL --------
    return ft.Column([
        ft.Text("Datos de familiares", size=20, weight="bold"),

        tabla_scroll,

        ft.Row([nombres, apellidos, movilidad], wrap=True),
        ft.Row([documento, celular, etnia], wrap=True),
        ft.Row([genero, nivel_educacion, fecha_nacimiento, btn_fecha], wrap=True),
        ft.Row([edad, estado_civil, discapacidad], wrap=True),
        ft.Row([enfermedad, trabaja, ocupacion], wrap=True),
        ft.Row([ingreso, parentesco], wrap=True),

        ft.ElevatedButton("Añadir familiar", on_click=add_familiar)
    ]), obtener_familiares
