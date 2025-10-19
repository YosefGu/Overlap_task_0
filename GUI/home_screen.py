import flet as ft



class HomeScreen:
    def __init__(self, page: ft.Page, set_path):
        self.page = page
        self.set_path = set_path
        self.message = ft.Text("", size=16)
        self.container = self.build()

    def build(self):
        title = ft.Text("Welcome", size=34, weight=ft.FontWeight.BOLD)
        description = ft.Text(
            "Select a flight log file (.bin) to analyze and view the flight path on the map.",
            size=20,
            color=ft.Colors.GREY_800,
        )

        choose_btn = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Text("Choose file", size=16),
                    ft.Icon(ft.Icons.UPLOAD_FILE)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
           ,
            width=150,
            height=50,
            on_click=lambda e: self.pick_file(),
        )

        card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [title, description, ft.Divider(), self.message, choose_btn],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=100,
                margin=50,
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

    # Logic
    def pick_file(self):
        file_picker = ft.FilePicker(on_result=self.on_file_picked)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(allowed_extensions=["bin"])

    def on_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.set_path(e.files[0].path)
            self.page.go('/map')
        else:
            self.message.value = "No file selected."
            self.page.update()

