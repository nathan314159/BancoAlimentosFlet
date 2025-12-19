import flet as ft

def consentimiento_view(on_toggle):
    checkbox = ft.Checkbox(value=False)

    row = ft.Row(
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            checkbox,
            ft.Column(
                expand=True,
                controls=[
                    ft.Text(
                        "Declaro que he sido informado(a) sobre el objetivo de esta encuesta y "
                        "doy mi consentimiento para proporcionar mis datos personales.",
                        size=18,
                    )
                ],
            ),
        ],
    )

    checkbox.on_change = on_toggle

    return row, checkbox
