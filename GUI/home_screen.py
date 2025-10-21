"""flet module for rendring UI"""

import flet as ft
from GUI.components.button import create_styled_button
from GUI.components.container import create_styled_container


class HomeScreen:
    """
    Home screen UI for selecting a flight log file.

    Public methods:
    - run(): builds the container

    Private methods:
    - _build(): builds the view
    - pick_file(): open a dialog for choosing bin file
    - _on_file_picked(): handle file picked
    """

    def __init__(self, page: ft.Page):
        self.page = page
        self.message = ft.Text("", size=16)
        self.container = self._build()

    def _build(self) -> ft.Container:
        """Create page with title, description, and choose file button."""
        title = ft.Text("Welcome", size=34, weight=ft.FontWeight.BOLD, color="#3383C4")

        description = ft.Text(
            "Select a flight log file (.bin) to analyze and view the flight path on the map.",
            size=18,
            color=ft.Colors.GREY_700,
            text_align=ft.TextAlign.CENTER,
        )

        choose_btn = create_styled_button(
            "Choose file", self._pick_file, ft.Icon(ft.Icons.UPLOAD_FILE)
        )
        card_content = ft.Container(
            content=ft.Column(
                [title, description, ft.Divider(), self.message, choose_btn],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=100,
            margin=75,
            border_radius=15,
            bgcolor="#B6D5DE",
            shadow=ft.BoxShadow(blur_radius=8, spread_radius=2, color=ft.Colors.GREY_200),
        )
        return create_styled_container(card_content)

    # Logic
    def _pick_file(self, e) -> None:
        """open file picker dialog."""
        file_picker = ft.FilePicker(on_result=self._on_file_picked)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(allowed_extensions=["bin"])

    def _on_file_picked(self, e: ft.FilePickerResultEvent) -> None:
        """handle the file picker event"""
        if e.files:
            self.page.client_storage.set("path", e.files[0].path)
            self.page.go("/map")
        else:
            self.message.value = "No file selected."
            self.page.update()
