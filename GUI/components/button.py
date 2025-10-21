"""
Button component for the Flet UI.

Provides helper functions to create consistently styled buttons
across the application.
"""
from typing import Callable
import flet as ft


def create_styled_button(text: str, on_click: Callable, icon: ft.Icon = None) -> ft.ElevatedButton:
    """
    Create a consistent styled ElevatedButton with icon and text.

    Args:
        text (str): Button text.
        icon (ft.Icon): Icon to display.
        on_click (callable): Function to call when clicked.

    Returns:
        ft.ElevatedButton: Styled button.
    """
    row_items = [ft.Text(text, size=16, weight=ft.FontWeight.W_500)]
    if icon:
        row_items.append(icon)

    return ft.ElevatedButton(
        content=ft.Row(row_items, alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        width=160,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10),
            overlay_color=ft.Colors.BLUE_400,
        ),
        on_click=on_click,
    )
