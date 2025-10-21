"""
Map screen module for displaying flight path on map using Flet and Flet Map.
"""

import asyncio

import flet as ft
import flet_map
import pandas as pd

from Business_logic.file_handling import FileHandling
from GUI.components.button import create_styled_button
from GUI.components.container import create_styled_container


class MapScreen:
    """
    Screen to display a map and flight points loaded from a .bin file.

    Public methods:
        - container: ft.Container with map and controls.

    Private methods:
        - _build(): builds the UI layout
        - _load_updated_screen(): async loading of points
        - _update_map_with_points(): render polylines on the map
        - _get_df_points(): extract points from file
        - _show_error(): display error message
        - _show_success(): display success message
    """

    def __init__(self, page: ft.Page):
        """
        Initialize MapScreen with Flet page.

        Args:
            page (ft.Page): Flet page instance.
        """
        self.page = page
        self.map_widget: flet_map.Map | None = None
        self.polyline_ref = ft.Ref[flet_map.PolylineLayer]()
        self.message_box: ft.Column | None = None

        self.container = self._build()
        self.page.run_task(self._load_updated_screen)

    async def _load_updated_screen(self) -> None:
        """
        Async function to load points in background and update the map.
        """
        try:
            df_points = await asyncio.to_thread(self._get_df_points)
            await asyncio.to_thread(self._update_map_with_points, df_points)
            self._show_success()
        except (ValueError, IOError) as e:
            self._show_error(str(e))
            return None
        except Exception as e:
            self._show_error(str(e))
            return None
        finally:
            self.page.update()

    def _build(self) -> ft.Container:
        """
        Build the map screen UI including back button, map widget, and message box.

        Returns:
            ft.Container: main container
        """
        back_button = create_styled_button("Back", lambda e: self.page.go("/"))

        self.map_widget = flet_map.Map(
            expand=True,
            initial_center=flet_map.MapLatitudeLongitude(32, 34.7),
            initial_zoom=8,
            layers=[
                flet_map.TileLayer(url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png"),
                flet_map.PolylineLayer(polylines=[], ref=self.polyline_ref),
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
        return create_styled_container(card_content)

    def _show_error(self, error: str) -> None:
        """
        Display an error message in the message box.

        Args:
            error (str): Error message text.
        """
        self.message_box.controls = [
            ft.Text(f"Error:{error}", size=16, color=ft.Colors.BLUE_700),
            ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED_400),
        ]
        self.page.update()

    def _show_success(self) -> None:
        """
        Display a success message in the message box.
        """
        self.message_box.controls = [
            ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
            ft.Text("Points loaded successfully!", size=16, color=ft.Colors.GREEN),
        ]

    def _update_map_with_points(self, points: pd.DataFrame) -> None:
        """
        Update the map widget with flight points as a polyline.

        Args:
            points (pd.DataFrame): DataFrame containing 'Lat' and 'Lng' columns.
        """
        coordinates = list(
            flet_map.MapLatitudeLongitude(lat, lon)
            for lat, lon in zip(points["Lat"].values, points["Lng"].values)
        )
        self.polyline_ref.current.polylines = [
            flet_map.PolylineMarker(
                coordinates, border_color="#5A58A6", color="#1A167E", border_stroke_width=4
            )
        ]
        self.map_widget.move_to(destination=coordinates[0], zoom=10, animation_duration=700)

    def _get_df_points(self) -> pd.DataFrame | None:
        """
        Load flight points from the selected .bin file.

        Returns:
            pd.DataFrame | None: DataFrame with points or None on failure.
        """
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
        except (ValueError, IOError) as e:
            self._show_error(str(e))
            return None
        except Exception as e:
            self._show_error(str(e))
            return None
