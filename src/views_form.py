import flet as ft
from views_consentimiento import consentimiento_view
from views_ubicacion import ubicacion_view
from views_familiares import familiares_view
from views_datos_vivienda_form import datos_vivienda_form
from data_base_insert import insert_datos_generales
import uuid
from sync_service import sincronizar_encuestas
from helper import *

def main(page: ft.Page):
    page.title = "Formulario de Datos Generales"
    page.scroll = "auto"
    page.padding = 20

    formulario_completo = ft.Column(visible=False)

    def toggle_form(e):
        formulario_completo.visible = e.control.value
        formulario_completo.update()

    consentimiento, checkbox = consentimiento_view(toggle_form)

    # ---- VISTAS ----
    ubicacion_ui, get_ubicacion = ubicacion_view(page)
    familiares_ui, get_familiares = familiares_view(page)
    vivienda_ui, get_vivienda, validar_vivienda, tablaVehiculos = datos_vivienda_form(page)

    def enviar(e):
        print(">>> CLICK EN ENVIAR")

        print("checkbox.value =", checkbox.value)
        print("validar_vivienda() =", validar_vivienda())

        if not checkbox.value:
            print(">>> NO aceptó consentimiento")
            page.snack_bar = ft.SnackBar(
                ft.Text("Debe aceptar el consentimiento informado")
            )
            page.snack_bar.open = True
            page.update()
            return

        if not validar_vivienda():
            print(">>> NO pasó validación de vivienda")
            page.snack_bar = ft.SnackBar(
                ft.Text("Complete los datos de la vivienda")
            )
            page.snack_bar.open = True
            page.update()
            return

        print(">>> PASÓ VALIDACIONES")
        


        uuid_encuesta = str(uuid.uuid4())

        data_vivienda = get_vivienda()
        print(">>> data_vivienda crudo:", data_vivienda)

        # 🔹 CONVERSIÓN DE CAMPOS NUMÉRICOS
        data_vivienda["datos_cuarto"] = safe_int(data_vivienda["datos_cuarto"])
        data_vivienda["datos_pago_vivienda"] = money_to_int(data_vivienda["datos_pago_vivienda"])
        data_vivienda["datos_pago_agua"] = money_to_int(data_vivienda["datos_pago_agua"])
        data_vivienda["datos_pago_luz"] = money_to_int(data_vivienda["datos_pago_luz"])
        data_vivienda["datos_cantidad_luz"] = safe_int(data_vivienda["datos_cantidad_luz"])
        data_vivienda["datos_pago_internet"] = money_to_int(data_vivienda["datos_pago_internet"])
        data_vivienda["datos_tv_pago"] = money_to_int(data_vivienda["datos_tv_pago"])
        data_vivienda["datos_gastos_viveres"] = money_to_int(data_vivienda["datos_gastos_viveres"])
        data_vivienda["datos_cantidad_celulare"] = safe_int(data_vivienda["datos_cantidad_celulare"])

        # Convierte los nombres en IDs usando la búsqueda flexible
        data_vivienda["datos_tipo_viviendas"] = get_item_ids_flexible(
            data_vivienda["datos_tipo_viviendas"], 22
        )[0] if get_item_ids_flexible(data_vivienda["datos_tipo_viviendas"], 22) else 0

        data_vivienda["datos_techos"] = get_item_ids_flexible(
            data_vivienda["datos_techos"], 23
        )[0] if get_item_ids_flexible(data_vivienda["datos_techos"], 23) else 0

        data_vivienda["datos_paredes"] = get_item_ids_flexible(
            data_vivienda["datos_paredes"], 24
        )[0] if get_item_ids_flexible(data_vivienda["datos_paredes"], 24) else 0

        data_vivienda["datos_pisos"] = get_item_ids_flexible(
            data_vivienda["datos_pisos"], 25
        )[0] if get_item_ids_flexible(data_vivienda["datos_pisos"], 25) else 0

        data_vivienda["datos_combustibles_cocina"] = get_item_ids_flexible(
            data_vivienda["datos_combustibles_cocina"], 26
        )[0] if get_item_ids_flexible(data_vivienda["datos_combustibles_cocina"], 26) else 0

        data_vivienda["datos_servicios_higienicos"] = get_item_ids_flexible(
            data_vivienda["datos_servicios_higienicos"], 27
        )[0] if get_item_ids_flexible(data_vivienda["datos_servicios_higienicos"], 27) else 0

        data_vivienda["datos_viviendas"] = get_item_ids_flexible(
            data_vivienda["datos_viviendas"], 28
        )[0] if get_item_ids_flexible(data_vivienda["datos_viviendas"], 28) else 0
        uuid_encuesta = str(uuid.uuid4())
        
        data_vivienda["datos_agua"] = get_item_ids_flexible(
            data_vivienda["datos_agua"], 29
        )[0] if get_item_ids_flexible(data_vivienda["datos_agua"], 29) else 0
        uuid_encuesta = str(uuid.uuid4())
        
        data_vivienda["datos_eliminacion_basura"] = get_item_ids_flexible(
            data_vivienda["datos_eliminacion_basura"], 30
        )[0] if get_item_ids_flexible(data_vivienda["datos_eliminacion_basura"], 30) else 0
        uuid_encuesta = str(uuid.uuid4())
        
        data_vivienda["datos_lugares_viveres"] = get_item_ids_flexible(
            data_vivienda["datos_lugares_viveres"], 31
        )[0] if get_item_ids_flexible(data_vivienda["datos_lugares_viveres"], 31) else 0
        uuid_encuesta = str(uuid.uuid4())
        
        data = {
            "uuid": uuid_encuesta,
            **get_ubicacion(),
            "familiares": get_familiares(),
            # **get_vivienda(),
            **data_vivienda,
        }

        print(">>> DATA ARMADA:", data)

        try:
            last_id = insert_datos_generales(data, tablaVehiculos)
            print(">>> ID INSERTADO:", last_id)

            page.snack_bar = ft.SnackBar(
                ft.Text("Formulario guardado correctamente")
            )

        except Exception as e:
            print(">>> ERROR REAL:", e)
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Error al guardar: {e}")
            )

        page.snack_bar.open = True
        page.update()

    def btn_sincronizar(e):
        sincronizar_encuestas()
        page.snack_bar = ft.SnackBar(
            ft.Text("Sincronización ejecutada")
        )
        page.snack_bar.open = True
        page.update()


    formulario_completo.controls = [
        ubicacion_ui,
        ft.Divider(),
        familiares_ui,
        ft.Divider(),
        vivienda_ui,
        ft.Divider(),
        ft.Row(
            controls=[
                ft.ElevatedButton("Enviar formulario", on_click=enviar),
                ft.ElevatedButton(
                    "Sincronizar",
                    icon=ft.Icons.SYNC,
                    on_click=btn_sincronizar
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
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
