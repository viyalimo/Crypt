import flet as ft
from back.Router import Router

def main(page: ft.Page):
    page.window.resizable = False
    page.window.height = 700
    page.window.width = 1200
    page.title = "Криптоконтейнер"
    LG = Router(page)


if __name__ == "__main__":
    ft.app(target=main)
