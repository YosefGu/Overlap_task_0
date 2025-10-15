import flet as ft
from home_screen import home_screen
from map_screen import map_screen


def main(page: ft.Page):
    page.bgcolor = '#A1CDED'
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def load_home():
        page.clean()
        page.add(home_screen(page, lambda e: load_map()))

    def load_map():
        locations = [
            (32.0853, 34.7818, "תל אביב"),
            (31.7683, 35.2137, "ירושלים"),
            (32.7940, 34.9896, "חיפה")
        ]
        page.clean()
        page.add(map_screen(page ,lambda e: load_home(), locations))

    load_home()

ft.app(target=main, view=ft.FLET_APP)
