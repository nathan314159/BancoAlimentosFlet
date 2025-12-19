

import flet as ft
from views_consentimiento import consentimiento_view
from views_ubicacion import ubicacion_view
from views_familiares import familiares_view
from views_datos_vivienda_form import datos_vivienda_form

def main(page: ft.Page):
    page.title = "Formulario de Datos Generales"
    page.scroll = "auto"
    page.padding = 20

    formulario_completo = ft.Column(visible=False)

    def toggle_form(e):
        formulario_completo.visible = e.control.value
        page.update()

    consentimiento, checkbox = consentimiento_view(toggle_form)

    formulario_completo.controls = [
        ubicacion_view(page),
        ft.Divider(),
        familiares_view(page),
        ft.Divider(),
        datos_vivienda_form(page),
    ]

    page.add(
        ft.Column(
            controls=[
                consentimiento,
                ft.Divider(),
                formulario_completo,
            ]
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
