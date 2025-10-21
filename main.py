import flet as ft

from router import AppRouter


def main(page: ft.Page) -> None:
    router = AppRouter(page)


ft.app(target=main, view=ft.FLET_APP)
