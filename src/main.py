import flet as ft

# Importar tu vista principal
from views_form import main as form_main

def main(page: ft.Page):
    page.title = "Banco de Alimentos Imbabura"
    page.scroll = "auto"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    return form_main(page)

if __name__ == "__main__":
    ft.app(target=main)