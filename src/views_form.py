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

    btn_sync = ft.ElevatedButton(text="🔄 Sincronizar", icon=ft.Icons.SYNC)

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
    # ---- VISTAS ----
    ubicacion_ui, get_ubicacion = ubicacion_view(page)
    familiares_ui, get_familiares = familiares_view(page)

    # Llamada a datos_vivienda_form pasando get_familiares
    vivienda_ui, get_vivienda, validar_vivienda, tablaVehiculos, datos_resultado_sistema, criterioMensaje = datos_vivienda_form(page, get_familiares)



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

        # UUID de la encuesta
        uuid_encuesta = str(uuid.uuid4())
        data_vivienda = get_vivienda()
        familiares = get_familiares()

        # Convertir tipos de datos
        INT_FIELDS = ["datos_cuarto", "datos_cantidad_luz", "datos_cantidad_celulare"]
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

        # Convertir catálogos a IDs
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

        for campo, catalogo_id in CATALOGOS_VIVIENDA.items():
            data_vivienda[campo] = map_catalogo(data_vivienda.get(campo), catalogo_id)

        # Normalizar familiares
        for familiar in familiares:
            familiar["datos_parentesco_etnia"] = safe_int(familiar.get("datos_parentesco_etnia", 0))
            familiar["datos_parentesco_genero"] = safe_int(familiar.get("datos_parentesco_genero", 0))
            familiar["datos_parentesco_nivel_educacion"] = safe_int(familiar.get("datos_parentesco_nivel_educacion", 0))
            familiar["datos_parentesco_estado_civil"] = safe_int(familiar.get("datos_parentesco_estado_civil", 0))
            familiar["fecha_nacimiento"] = convertir_fecha(familiar.get("fecha_nacimiento"))

        data_vivienda["ingreso_mensual"] = sum(
            safe_float(f.get("ingreso")) for f in familiares
        )
        
        # Armar datos finales
        data = {
            "uuid": uuid_encuesta,
            **get_ubicacion(),
            "familiares": familiares,
            **data_vivienda,
        }
        
        
        
        print(">>> DATA ARMADA:", data)
        
        

        
        # Datos de vehículos
        tabla_vehiculos_data = [
            {"datos_estado_transporte": row.cells[1].content.value} for row in tablaVehiculos.rows
        ]

        # Evaluar resultado
        resultado_sistema, mensaje_criterio = evaluar_resultado(
            tabla_parentesco=[{"ingreso_mensual": float(data_vivienda.get("ingreso_mensual") or 0)}],
            tabla_vehiculos=tabla_vehiculos_data,
            datos_pago_vivienda=data_vivienda.get("datos_pago_vivienda"),
            datos_pago_agua=data_vivienda.get("datos_pago_agua"),
            datos_pago_luz=data_vivienda.get("datos_pago_luz"),
            datos_pago_internet=data_vivienda.get("datos_pago_internet"),
            datos_tv_pago=data_vivienda.get("datos_tv_pago"),
            datos_gastos_viveres_alimentacion=data_vivienda.get("datos_gastos_viveres"),
            id_datos_generales=1,
        )

        # Actualizar UI
        datos_resultado_sistema.value = resultado_sistema
        datos_resultado_sistema.update()
        criterioMensaje.value = mensaje_criterio
        criterioMensaje.update()

        # Guardar en DB
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
        ok, mensaje = sincronizar_encuestas()

        actualizar_estado_sync()
        page.update()
        if not ok:
            page.open(
                ft.SnackBar(
                    content=ft.Text(mensaje),
                    bgcolor=ft.Colors.RED_600,
                    duration=4000,
                    show_close_icon=True,
                )
            )
            return

        page.open(
            ft.SnackBar(
                content=ft.Text(mensaje),
                bgcolor=ft.Colors.GREEN_600,
                duration=4000,
            )
        )

    btn_sync.on_click = btn_sincronizar

    formulario_completo.controls = [
        ubicacion_ui,
        ft.Divider(),
        familiares_ui,
        ft.Divider(),
        vivienda_ui,
        ft.Divider(),
        ft.Row(
            controls=[ft.ElevatedButton("Enviar formulario", on_click=enviar)]
        ),
    ]

    def actualizar_estado_sync():
        pendientes = contar_pendientes()
        btn_sync.text = f"🔄 Sincronizar ({pendientes} pendientes)"
        btn_sync.update()

    page.add(
        ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[btn_sync],
                ),
                ft.Divider(),
                consentimiento,
                ft.Divider(),
                formulario_completo,
            ],
        )
    )
    actualizar_estado_sync()


if __name__ == "__main__":
    ft.app(target=main)
