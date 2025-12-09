from data_base_models import get_etnia, get_genero, get_educacion, get_estado_civil
from datetime import datetime
import flet as ft

# -------------------------
# VALIDAR CÉDULA ECUATORIANA
# -------------------------
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


# ===========================
#     FAMILIARES VIEW
# ===========================
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
    nombres = ft.TextField(label="Nombres", width=260)
    apellidos = ft.TextField(label="Apellidos", width=260)
    movilidad = ft.Dropdown(
        label="Movilidad", width=260,
        options=[
            ft.dropdown.Option("Ecuatoriano"),
            ft.dropdown.Option("Extranjero")
        ]
    )
    documento = ft.TextField(label="Documento", width=260, disabled=True)
    celular = ft.TextField(label="Celular", width=260)

    etnia = ft.Dropdown(label="Etnia", width=260)
    genero = ft.Dropdown(label="Género", width=260)
    nivel_educacion = ft.Dropdown(label="Nivel Educación", width=260)
    estado_civil = ft.Dropdown(label="Estado Civil", width=260)

    # -------- FECHA NACIMIENTO --------
    fecha_nacimiento = ft.TextField(label="Fecha Nacimiento", width=260, read_only=True)

    date_picker = ft.DatePicker(
        on_change=lambda e: (
            setattr(fecha_nacimiento, "value", e.control.value),
            fecha_nacimiento.update()
        )
    )
    page.overlay.append(date_picker)

    btn_fecha = ft.IconButton(
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: setattr(date_picker, "open", True) or page.update()
    )

    edad = ft.TextField(label="Edad", width=260)

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
        on_change=on_discapacidad_change
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

    ocupacion = ft.TextField(label="Ocupación", width=260, disabled=True)

    ingreso = ft.TextField(label="Ingreso Mensual", width=260)
    parentesco = ft.TextField(label="Parentesco", width=260)

    # -------- CARGAR BD --------
    etnia.options = [ft.dropdown.Option(i) for i in get_etnia()]
    genero.options = [ft.dropdown.Option(i) for i in get_genero()]
    nivel_educacion.options = [ft.dropdown.Option(i) for i in get_educacion()]
    estado_civil.options = [ft.dropdown.Option(i) for i in get_estado_civil()]
    page.update()

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

    def add_familiar(e):

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
        page.update()

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

        ft.Row([nombres, apellidos, documento], wrap=True),
        ft.Row([celular, etnia, genero], wrap=True),
        ft.Row([nivel_educacion, fecha_nacimiento, btn_fecha], wrap=True),
        ft.Row([edad, estado_civil, discapacidad], wrap=True),
        ft.Row([enfermedad, trabaja, ocupacion], wrap=True),
        ft.Row([ingreso, parentesco], wrap=True),

        ft.ElevatedButton("Añadir familiar", on_click=add_familiar)
    ])
