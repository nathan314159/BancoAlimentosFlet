# Formulario de voluntario
from views_familiares import familiares_view
from data_base_models import get_provincias, get_cantones_by_provincia, get_parroquias_by_canton_and_tipo

import flet as ft

def main(page: ft.Page):
    page.title = "Formulario de Datos Generales"
    page.scroll = "auto"
    page.padding = 20

    # ---------------------------------------------------------
    # BASE
    # ---------------------------------------------------------
    consentimiento_chk = ft.Checkbox(
        label="Declaro que he sido informado(a) sobre el objetivo de esta encuesta y doy mi consentimiento para proporcionar mis datos personales.",
        value=False,
        width=380
    )


    # Dropdowns
    ddl_provincia = ft.Dropdown(
        label="Provincia",
        width=250,
        options=[ft.dropdown.Option(p) for p in get_provincias()]
    )

    ddl_canton = ft.Dropdown(
        label="Cantón",
        width=250,
        options=[]
    )

    ddl_tipo_parroquia = ft.Dropdown(
        label="Tipo de Parroquia",
        width=250,
        options=[
            ft.dropdown.Option("Urbano"),
            ft.dropdown.Option("Rural")
        ],
        disabled=True  # empieza deshabilitado hasta que el usuario elija un cantón
    )

    ddl_parroquia = ft.Dropdown(
        label="Parroquia",
        width=250,
        options=[],
        disabled=True
    )

    # ---------------------------------------------------------
    # EVENTO — CAMBIAR PROVINCIA
    # ---------------------------------------------------------

    def provincia_changed(e):
        provincia = ddl_provincia.value
        cantones = get_cantones_by_provincia(provincia)

        ddl_canton.options = [ft.dropdown.Option(c) for c in cantones]
        ddl_canton.value = None

        ddl_tipo_parroquia.disabled = True
        ddl_parroquia.disabled = True

        page.update()

    ddl_provincia.on_change = provincia_changed


    # ---------------------------------------------------------
    # EVENTO — CAMBIAR CANTÓN
    # ---------------------------------------------------------
    def canton_changed(e):
        ddl_tipo_parroquia.disabled = False
        ddl_tipo_parroquia.value = None

        ddl_parroquia.disabled = True
        ddl_parroquia.options = []
        ddl_parroquia.value = None

        page.update()

    ddl_canton.on_change = canton_changed


    # ---------------------------------------------------------
    # EVENTO — CAMBIAR TIPO PARROQUIA (Urbano/Rural)
    # ---------------------------------------------------------
    def tipo_parroquia_changed(e):
        canton = ddl_canton.value
        tipo = ddl_tipo_parroquia.value

        parroquias = get_parroquias_by_canton_and_tipo(canton, tipo)

        ddl_parroquia.options = [ft.dropdown.Option(p) for p in parroquias] 
        # print(ddl_parroquia)
        ddl_parroquia.disabled = False
        ddl_parroquia.value = None

        page.update()

    ddl_tipo_parroquia.on_change = tipo_parroquia_changed

    # ---------------------------------------------------------
    # CONTENEDOR DEL FORMULARIO COMPLETO (oculto al inicio)
    # ---------------------------------------------------------
    formulario_completo = ft.Column(
        visible=False,
        controls=[
            ft.Text("Formulario para datos generales y parentescos",
                    size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),

            ft.Row(
                controls=[
                    ddl_provincia,
                    ddl_canton,
                    ddl_tipo_parroquia,
                    ddl_parroquia,
                ],
                wrap=True,
            ),
            ft.Divider(),
            familiares_view(page),
            ft.Divider(),
        ]
    )

    # ---------------------------------------------------------
    # MOSTRAR/OCULTAR FORMULARIO
    # ---------------------------------------------------------
    def toggle_form(e):
        formulario_completo.visible = consentimiento_chk.value
        page.update()

    consentimiento_chk.on_change = toggle_form

    # ---------------------------------------------------------
    # AGREGA TODO
    # ---------------------------------------------------------
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Formulario para datos generales y parentescos",
                            size=20, weight=ft.FontWeight.BOLD, text_align="center"),
                    ft.Divider(),
                    consentimiento_chk,
                    ft.Divider(),
                    formulario_completo
                ]
            )
        )
    )
if __name__ == "__main__":
    import flet as ft
    ft.app(target=main)


