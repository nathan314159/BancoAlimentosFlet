import flet as ft
from views_consentimiento import consentimiento_view
from views_ubicacion import ubicacion_view
from views_familiares import familiares_view
from views_datos_vivienda_form import datos_vivienda_form
from data_base_insert import insert_datos_generales
import uuid
from sync_service import sincronizar_encuestas
from helper import *
import os
import sqlite3
def main(page: ft.Page):
    page.title = "Formulario de Datos Generales"
    page.scroll = "auto"
    page.padding = 20

    formulario_completo = ft.Column(visible=False)
    
    estado_sync_txt = ft.Text(
        value="⏳ Verificando encuestas pendientes...",
        size=12,
        color=ft.Colors.GREY
    )

    def contar_pendientes():
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DB_PATH = os.path.join(BASE_DIR, "app.db")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM tbl_datos_generales_PRUEBA WHERE sincronizado = 0"
        )
        total = cursor.fetchone()[0]
        conn.close()
        return total

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
            page.open(
                ft.SnackBar(
                    content=ft.Text("Debe aceptar el consentimiento informado"),
                    duration=4000
                )
            )
            return

        if not validar_vivienda():
            print(">>> NO pasó validación de vivienda")
            page.open(
                ft.SnackBar(
                    content=ft.Text("Complete los datos de la vivienda"),
                    duration=4000
                )
            )
            return

        print(">>> PASÓ VALIDACIONES")
        
        
        CATALOGOS_VIVIENDA = {
            "datos_tipo_viviendas": 22,
            "datos_techos": 23,
            "datos_paredes": 24,
            "datos_pisos": 25,
            "datos_combustibles_cocina": 26,
            "datos_servicios_higienicos": 27,
            "datos_viviendas": 28,
            "datos_agua": 29,
            "datos_eliminacion_basura": 30,
            "datos_lugares_viveres": 31,
        }
                
        def map_catalogo(valor, catalogo_id):
            ids = get_item_ids_flexible(valor, catalogo_id)
            return ids[0] if ids else 0

        uuid_encuesta = str(uuid.uuid4())

        data_vivienda = get_vivienda()
        familiares  = get_familiares()

        print(">>> data_vivienda crudo:", data_vivienda)

        # 🔹 CONVERSIÓN DE CAMPOS NUMÉRICOS
        # data_vivienda["datos_cuarto"] = safe_int(data_vivienda["datos_cuarto"])
        # data_vivienda["datos_pago_vivienda"] = money_to_int(data_vivienda["datos_pago_vivienda"])
        # data_vivienda["datos_pago_agua"] = money_to_int(data_vivienda["datos_pago_agua"])
        # data_vivienda["datos_pago_luz"] = money_to_int(data_vivienda["datos_pago_luz"])
        # data_vivienda["datos_cantidad_luz"] = safe_int(data_vivienda["datos_cantidad_luz"])
        # data_vivienda["datos_pago_internet"] = money_to_int(data_vivienda["datos_pago_internet"])
        # data_vivienda["datos_tv_pago"] = money_to_int(data_vivienda["datos_tv_pago"])
        # data_vivienda["datos_gastos_viveres"] = money_to_int(data_vivienda["datos_gastos_viveres"])
        # data_vivienda["datos_cantidad_celulare"] = safe_int(data_vivienda["datos_cantidad_celulare"])
        
        INT_FIELDS = [
            "datos_cuarto",
            "datos_cantidad_luz",
            "datos_cantidad_celulare",
        ]

        MONEY_FIELDS = [
            "datos_pago_vivienda",
            "datos_pago_agua",
            "datos_pago_luz",
            "datos_pago_internet",
            "datos_tv_pago",
            "datos_gastos_viveres",
        ]

        for field in INT_FIELDS:
            data_vivienda[field] = safe_int(data_vivienda.get(field))

        for field in MONEY_FIELDS:
            data_vivienda[field] = money_to_int(data_vivienda.get(field))


        # Convierte los nombres en IDs usando la búsqueda flexible
        for campo, catalogo_id in CATALOGOS_VIVIENDA.items():
            data_vivienda[campo] = map_catalogo(
                data_vivienda.get(campo),
                catalogo_id
            )

        
        # Convierte los nombres en IDs usando la búsqueda flexible (PARENTESCO)

        for familiar in familiares:
            familiar["datos_parentesco_etnia"] = safe_int(
                familiar.get("datos_parentesco_etnia", 0)
            )
            familiar["datos_parentesco_genero"] = safe_int(
                familiar.get("datos_parentesco_genero", 0)
            )
            familiar["datos_parentesco_nivel_educacion"] = safe_int(
                familiar.get("datos_parentesco_nivel_educacion", 0)
            )
            familiar["datos_parentesco_estado_civil"] = safe_int(
                familiar.get("datos_parentesco_estado_civil", 0)
            )
            
            familiar["fecha_nacimiento"] = convertir_fecha(
                familiar.get("fecha_nacimiento")
            )

            
            print(
                "FECHA FINAL PYTHON 👉",
                familiar.get("datos_parentesco_fecha_de_nacimiento"),
                type(familiar.get("datos_parentesco_fecha_de_nacimiento"))
            )
            


        data = {
            "uuid": uuid_encuesta,
            **get_ubicacion(),
            "familiares": familiares,
            # **get_vivienda(),
            **data_vivienda,
        }

        print(">>> DATA ARMADA:", data)

        try:
            last_id = insert_datos_generales(data, tablaVehiculos)
            print(">>> ID INSERTADO:", last_id)

            page.open(
                ft.SnackBar(
                    content=ft.Text("✅ Formulario guardado correctamente"),
                    bgcolor=ft.Colors.GREEN_600,
                    duration=4000
                )
            )
            actualizar_estado_sync()

        except Exception as e:
            page.open(
                ft.SnackBar(
                    content=ft.Text(f"❌ Error al guardar: {e}"),
                    bgcolor=ft.Colors.RED_600,
                    duration=4000
                )
            )






    def btn_sincronizar(e):
        ok = sincronizar_encuestas()
        actualizar_estado_sync()
        page.update()

        if not ok:
            page.open(
                ft.SnackBar(
                    content=ft.Text(
                        "🚫 SERVIDOR NO DISPONIBLE (Apache apagado)"
                    ),
                    bgcolor=ft.Colors.RED_600,
                    show_close_icon=True,
                )
            )
            return

        page.open(
            ft.SnackBar(
                content=ft.Text("✅ Sincronizado correctamente"),
                bgcolor=ft.Colors.GREEN_600,
                duration=4000
            )
        )





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
            ],
        )
    ]
    

    def actualizar_estado_sync():
        pendientes = contar_pendientes()
        estado_sync_txt.value = f"📤 Encuestas pendientes: {pendientes}"
        estado_sync_txt.update()

            

    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "🔄 Sincronizar datos pendientes",
                            icon=ft.Icons.SYNC,
                            on_click=btn_sincronizar
                        ),
                        estado_sync_txt
                    ],
                    alignment=ft.MainAxisAlignment.END
                ),
                ft.Divider(),
                consentimiento,
                ft.Divider(),
                formulario_completo,
            ]
        )
    )
    actualizar_estado_sync()

if __name__ == "__main__":
    ft.app(target=main)
