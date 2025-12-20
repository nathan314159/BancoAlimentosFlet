import flet as ft
from data_base_models import (
    get_provincias,
    get_cantones_by_provincia,
    get_parroquias_by_canton_and_tipo,
)

def ubicacion_view(page: ft.Page):

    ddl_provincia = ft.Dropdown(
        label="Provincia",
        width=250,
        options=[ft.dropdown.Option(p) for p in get_provincias()],
    )

    ddl_canton = ft.Dropdown(label="Cantón", width=250)

    ddl_tipo_parroquia = ft.Dropdown(
        label="Tipo de Parroquia",
        width=250,
        options=[
            ft.dropdown.Option("Urbano"),
            ft.dropdown.Option("Rural"),
        ],
        disabled=True,
    )

    ddl_parroquia = ft.Dropdown(
        label="Parroquia",
        width=250,
        disabled=True,
    )

    # ---------------- EVENTS ----------------

    def provincia_changed(e):
        # 🔹 cargar cantones
        ddl_canton.options = [
            ft.dropdown.Option(c)
            for c in get_cantones_by_provincia(ddl_provincia.value)
        ]
        ddl_canton.value = None

        # 🔹 reset dependientes
        ddl_tipo_parroquia.value = None
        ddl_tipo_parroquia.disabled = True

        ddl_parroquia.value = None
        ddl_parroquia.options = []
        ddl_parroquia.disabled = True

        # 🔹 actualizar solo lo necesario
        ddl_canton.update()
        ddl_tipo_parroquia.update()
        ddl_parroquia.update()

    def canton_changed(e):
        ddl_tipo_parroquia.disabled = False
        ddl_tipo_parroquia.value = None

        ddl_parroquia.value = None
        ddl_parroquia.options = []
        ddl_parroquia.disabled = True

        ddl_tipo_parroquia.update()
        ddl_parroquia.update()

    def tipo_parroquia_changed(e):
        ddl_parroquia.options = [
            ft.dropdown.Option(p)
            for p in get_parroquias_by_canton_and_tipo(
                ddl_canton.value,
                ddl_tipo_parroquia.value
            )
        ]
        ddl_parroquia.value = None
        ddl_parroquia.disabled = False

        ddl_parroquia.update()

    ddl_provincia.on_change = provincia_changed
    ddl_canton.on_change = canton_changed
    ddl_tipo_parroquia.on_change = tipo_parroquia_changed

    def obtener_ubicacion():
        return {
            "provincia": ddl_provincia.value,
            "canton": ddl_canton.value,
            "tipo_parroquia": ddl_tipo_parroquia.value,
            "parroquia": ddl_parroquia.value,
        }

    return (
        ft.Row(
            wrap=True,
            controls=[
                ddl_provincia,
                ddl_canton,
                ddl_tipo_parroquia,
                ddl_parroquia,
            ],
        ),
        obtener_ubicacion
    )

