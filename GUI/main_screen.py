import sys
from pathlib import Path
base_path = Path(__file__).resolve().parent.parent
sys.path.append(str(base_path))

import flet as ft
from home_screen import home_screen
from map_screen import map_screen

def main(page: ft.Page):
    # page.bgcolor = '#A1CDED'
    # page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    locations = []

    def set_locations(new_locations):
        nonlocal locations
        locations = new_locations

    def route_change(e):
        index = None
        for i, view in enumerate(page.views):
            if view.route == page.route:
                index = i
                break

        if index:
            view = page.views.pop(index)
            page.views = page.views.append(view)
        else:
            if page.route == "/":
                page.views.append(
                    ft.View("/", [home_screen(page, set_locations)])
                )
            elif page.route == "/map":
                page.views.append(
                    ft.View("/map", [map_screen(page, locations)])
                )
        page.update()
    
    def view_pop(view):
        page.views.pop()
        page.update()
        # top_view = page.views[-1]
        # page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)

ft.app(target=main, view=ft.FLET_APP)
