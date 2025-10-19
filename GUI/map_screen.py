import flet as ft
import flet_map as map
from Business_logic.file_handling import FileHandling

class MapScreen:
    def __init__(self, page: ft.Page, path: str):
        self.page = page
        self.path = path
        self.message = None
        self.polyline_ref = ft.Ref[map.PolylineLayer]()
        self.map_widget = None
        self.container = self.build()

    def build(self):
        back_button = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Text("Back", size=16)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            width=150,
            height=50,
            on_click=lambda e: self.page.go('/')
        )
        self.message = ft.Column(
            [
                ft.Text("Loading points...", size=16, color=ft.Colors.BLUE_700),
                ft.ProgressBar(width=300, color=ft.Colors.BLUE_700)
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.map_widget = map.Map(
            expand=True,
            initial_center=map.MapLatitudeLongitude(32, 34.7),
            initial_zoom=8,
            layers=[
                map.TileLayer(url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png"),
                map.PolylineLayer(polylines=[], ref=self.polyline_ref)
            ]
        )

        card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [back_button, self.message, self.map_widget],
                    spacing=5,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                expand=True,
                padding=10,
                margin=30,
                border_radius=15,
                bgcolor="#B6D5DE",
                shadow=ft.BoxShadow(blur_radius=8, spread_radius=2, color=ft.Colors.GREY_200),
            )
        )
        return ft.Container(
            content=card,
            expand=True,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.BLUE_GREY_50,
        )
    
    def load_points(self):
        try:
            file_handling = FileHandling(self.path)
            points = file_handling.run()
            coordinates = [map.MapLatitudeLongitude(lat, lon) for lat, lon in points]
            # start_marker = map.Marker(
            #     coordinates=coordinates[0],
            #     content=ft.Icon(name=ft.Icons.PLAY_ARROW, color="#2F4BA4", size=32)
            # )
            # end_marker = map.Marker(
            #     coordinates=coordinates[-1],
            #     content=ft.Icon(name=ft.Icons.FLAG_CIRCLE, color="#FF0000", size=24)
            # )

            self.polyline_ref.current.polylines = [
                map.PolylineMarker(
                    coordinates=coordinates,
                    border_stroke_width=1,
                    border_color="#3330F0"
                )
            ]
            self.map_widget.move_to(
                destination=coordinates[0],
                zoom=10,
                animation_duration=700
            )
            self.message.controls = [
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
                ft.Text("Points loaded successfully!", size=16, color=ft.Colors.GREEN)
            ]
            self.page.update()
        except Exception as e:
            self.message.value = f"Error: {e}"
            self.page.update()
