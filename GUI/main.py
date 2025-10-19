import sys
from pathlib import Path
import flet as ft

base_path = Path(__file__).resolve().parent.parent
sys.path.append(str(base_path))

from home_screen import HomeScreen
from map_screen import MapScreen

def main(page: ft.Page):
    path = None

    def set_path(new_path):
        nonlocal path
        path = new_path
    
    def add_home_screen():
        home = HomeScreen(page, set_path)
        page.views.append(
                ft.View("/", [home.container])
            )
        page.update()

    def add_map_screen():
        map = MapScreen(page, path)
        page.views.append(
                ft.View("/map", [map.container])
            )
        page.update()
        map.load_points()
        page.update()

    def route_change(e):
        page.views.clear()
        if page.route == "/":
            add_home_screen()
        elif page.route == "/map":
            add_map_screen()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, view=ft.FLET_APP)
