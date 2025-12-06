import flet as ft

# Importar tu vista principal
from views.form_view import main as form_main

def main(page: ft.Page):
    return form_main(page)

if __name__ == "__main__":
    ft.app(target=main)