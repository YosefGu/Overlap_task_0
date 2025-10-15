import flet as ft

def home_screen(page: ft.Page, load_map):
    title = ft.Text("Welcome", size=24)
    description = ft.Text(
        "In this system you can select a flight log file and display it on a map.",
        size=18
    )
    file = ft.Text("", size=16)

    def pick_file():
        file_picker = ft.FilePicker(on_result=on_file_picked)
        page.overlay.append(file_picker)
        page.update()
        file_picker.pick_files(allowed_extensions=['bin'])          

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            file.value = f"Picked file: {e.files}"
        else:
            file.value = "No picked file"
        file.update()

    btn = ft.ElevatedButton("Choose file", on_click= lambda e: pick_file())

    btn_to_map = ft.ElevatedButton("Go to map", on_click=load_map)

    return ft.Column([title, description, file, btn, btn_to_map])
