import flet as ft

def money_input(label="Monto", value="", disabled=False, width=260 ):
    def validate_numeric(e):
        if field.disabled:   # 👈 CLAVE
            return
        
        txt = field.value.replace(",", "").replace(" ", "")

        # Allow empty while typing
        if txt == "":
            return
        
        # Allow digits and ONE decimal point
        if not txt.replace(".", "", 1).isdigit():
            field.value = prev_value[0]  # restore last valid value
        else:
            prev_value[0] = field.value  # keep latest valid

        e.page.update()

    def format_on_blur(e):
        txt = field.value.replace(",", "").replace(" ", "")
        if txt == "":
            field.value = ""
        else:
            number = float(txt)
            field.value = f"{number:,.2f}"
        e.page.update()

    prev_value = [""]  # store last valid input

    field = ft.TextField(
        label=label,
        value=value,
        on_change=validate_numeric,   # no formatting while typing
        on_blur=format_on_blur,       # format only when leaving the field
        keyboard_type=ft.KeyboardType.NUMBER,
        disabled=disabled,
        width=width
    )

    return field


def load_dropdown_options(control, items):
    control.options = [ft.dropdown.Option(i) for i in items]

def solo_letras(e):
    control = e.control
    if not control.value.replace(" ", "").isalpha():
        control.error_text = "Solo letras"
    else:
        control.error_text = None
    control.update()

def solo_numeros(e):
    control = e.control
    if not control.value.isdigit():
        control.error_text = "Solo números positivos"
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










