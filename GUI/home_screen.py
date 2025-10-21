import flet as ft


class HomeScreen:

    def __init__(self, page: ft.Page):
        self.page = page
        self.message = ft.Text("", size=16)
        self.container = self._build()

    def _build(self) -> ft.Container:
        title = ft.Text("Welcome", size=34, weight=ft.FontWeight.BOLD, color="#3383C4")

        description = ft.Text(
            "Select a flight log file (.bin) to analyze and view the flight path on the map.",
            size=18,
            color=ft.Colors.GREY_700,
            text_align=ft.TextAlign.CENTER,
        )

        choose_btn = ft.ElevatedButton(
            content=ft.Row(
                [ft.Text("Choose file", size=16, weight=ft.FontWeight.W_500), ft.Icon(ft.Icons.UPLOAD_FILE)],
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
            on_click=lambda e: self._pick_file(),
        )

        container = ft.Container(
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

        return ft.Container(
            content=container,
            expand=True,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.RED_50,
        )

    # Logic
    def _pick_file(self) -> None:
        file_picker = ft.FilePicker(on_result=self._on_file_picked)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(allowed_extensions=["bin"])

    def _on_file_picked(self, e: ft.FilePickerResultEvent) -> None:
        if e.files:
            self.page.client_storage.set("path", e.files[0].path)
            self.page.go("/map")
        else:
            self.message.value = "No file selected."
            self.page.update()
