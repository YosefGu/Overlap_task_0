import flet as ft
import tkinter as tk
from tkintermapview import TkinterMapView

def map_screen(page: ft.Page, load_home, locations: list):
    title = ft.Text("Map screen")
    btn = ft.ElevatedButton("Back home", on_click=load_home)

    column = ft.Column([title, btn], expand=True)
    page.add(column)


    return column


