import flet as ft

from GUI.home_screen import HomeScreen
from GUI.map_screen import MapScreen


class AppRouter:

    def __init__(self, page: ft.Page):
        self.page = page
        self._configure_page()

    def _configure_page(self) -> None:
        self.page.on_route_change = self._route_change
        self.page.go(self.page.route or "/")

    def _route_change(self, e: ft.ControlEvent) -> None:
        self.page.views.clear()
        if self.page.route == "/":
            self._add_home_screen()
        elif self.page.route == "/map":
            self._add_map_screen()

    def _add_home_screen(self) -> None:
        home = HomeScreen(self.page)
        self.page.views.append(ft.View("/", [home.container]))
        self.page.update()

    def _add_map_screen(self) -> None:
        map = MapScreen(self.page)
        self.page.views.append(ft.View("/map", [map.container]))
        self.page.update()

