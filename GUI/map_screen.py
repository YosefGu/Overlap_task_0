import flet as ft
import flet_map as map


def map_screen(page: ft.Page, locations: list):

    back_button = ft.ElevatedButton(
        "Back", 
        on_click=lambda _: page.on_view_pop(page.views[-1])
    )

    coordinates = [
        map.MapLatitudeLongitude(lat, lon) for lat, lon in locations
    ]

    circles = [
        map.CircleMarker(
            coordinates=coord,
            radius=3,
            color=ft.Colors.RED,
        ) for coord in coordinates
    ]

    start_marker = map.Marker(
        coordinates=coordinates[0],
        content=ft.Icon(
            name=ft.Icons.PLAY_ARROW,
            color="#2F4BA4",
            size=32
        )
    ) 

    end_marker = map.Marker(
        coordinates=coordinates[-1],
        content=ft.Icon(
            name=ft.Icons.FLAG_CIRCLE,
            color="#FF0000",
            size=32
        )
    ) 

    return ft.Column(
        [
            back_button,
            map.Map(
                expand=True,
                initial_center = coordinates[0],
                initial_zoom = 11,
                layers=[
                    map.TileLayer(
                        url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
                    ),
                    map.CircleLayer(
                        circles=circles
                    ),
                    map.PolylineLayer(
                        polylines=[
                            map.PolylineMarker(
                                coordinates=coordinates,
                                border_stroke_width=1,
                                border_color='#09FF00'
                            )
                        ]
                    ),
                    map.MarkerLayer(
                       markers=[
                           start_marker,
                           end_marker
                       ] 
                    )
                ],
            ),
        ],
        expand=True,
    )
