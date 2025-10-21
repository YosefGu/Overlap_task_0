import asyncio

import flet as ft
import flet_map as map
import pandas as pd

from Business_logic.file_handling import FileHandling


class MapScreen:

    def __init__(self, page: ft.Page):
        self.page = page
        self.map_widget: map.Map
        self.polyline_ref = ft.Ref[map.PolylineLayer]()
        self.message_box: ft.Column = None

        self.container = self._build()
        self.page.run_task(self._load_updated_screen)

    async def _load_updated_screen(self) -> None:
        try:
            df_points = await asyncio.to_thread(self._get_df_points)
            await asyncio.to_thread(self._update_map_with_points, df_points)
            self._show_success()
            self.page.update()
        except Exception as e:
            self._show_error(str(e))

    def _build(self) -> ft.Container:
        back_button = ft.ElevatedButton(
            content=ft.Row(
                [ft.Text("Back", size=16, weight=ft.FontWeight.W_500)],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            width=160,
            height=50,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=10),
                overlay_color=ft.Colors.BLUE_400,
            ),
            on_click=lambda e: self.page.go("/"),
        )

        self.map_widget = map.Map(
            expand=True,
            initial_center=map.MapLatitudeLongitude(32, 34.7),
            initial_zoom=8,
            layers=[
                map.TileLayer(url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png"),
                map.PolylineLayer(polylines=[], ref=self.polyline_ref),
            ],
        )

        self.message_box = ft.Column(
            [
                ft.Text("Loading points...", size=16, color=ft.Colors.BLUE_700),
                ft.ProgressBar(width=300, color=ft.Colors.BLUE_700),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        card_content = ft.Container(
            content=ft.Column(
                [back_button, self.message_box, self.map_widget],
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            padding=20,
            margin=75,
            border_radius=15,
            bgcolor="#B6D5DE",
            shadow=ft.BoxShadow(blur_radius=8, spread_radius=2, color=ft.Colors.GREY_200),
        )
        # )
        return ft.Container(
            content=card_content,
            expand=True,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.RED_50,
        )

    def _show_error(self, error: str) -> None:
        self.message_box.controls = [
            ft.Text(f"Error:{error}", size=16, color=ft.Colors.BLUE_700),
            ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED_400),
        ]
        self.page.update()

    def _show_success(self) -> None:
        self.message_box.controls = [
            ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
            ft.Text("Points loaded successfully!", size=16, color=ft.Colors.GREEN),
        ]

    def _update_map_with_points(self, points: pd.DataFrame) -> None:
        coordinates = list(
            map.MapLatitudeLongitude(lat, lon) for lat, lon in zip(points["Lat"].values, points["Lng"].values)
        )
        self.polyline_ref.current.polylines = [
            map.PolylineMarker(coordinates=coordinates, border_stroke_width=1, border_color="#3330F0")
        ]
        self.map_widget.move_to(destination=coordinates[0], zoom=10, animation_duration=700)

    def _get_df_points(self) -> pd.DataFrame | None:
        try:
            path = self.page.client_storage.get("path")
            if not path:
                self._show_error("No PATH found.")
                return None
            
            file_handling = FileHandling(path)
            points = file_handling.run()

            if points.empty:
                self._show_error("No GPS points found.")
                return None
            return points
        except Exception as e:
            self._show_error(str(e))
            return None
