"""
Container component for the Flet UI.

Provides helper functions to wrap content containers with
consistent styling for the application.
"""
import flet as ft


def create_styled_container(container: ft.Container) -> ft.Container:
    """
    Wraps a given Flet container with a consistent page-level style.

    This function helps maintain a unified look across the app by applying
    default styling such as centered alignment, full expansion, and
    background color.

    Args:
        container (ft.Container): The inner container or layout element to be wrapped.

    Returns:
        ft.Container: A styled container that centers and expands the given content
                      with a predefined background color.
    """
    return ft.Container(
        content=container,
        expand=True,
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.RED_50,
    )
