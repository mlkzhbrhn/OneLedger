import flet as ft


def asset_card(name, balance, flag_url):
    return ft.Container(
        # bgcolor=ft.Colors.WHITE,
        border_radius=10,
        width=150,
        margin=5,
        padding=10,
        content=ft.Column(
            [
                ft.CircleAvatar(
                    foreground_image_src=f"{flag_url}",
                    radius=24,
                ),
                ft.Text(f"{name} balance"),
                ft.Text(f"{balance} {name}"),
            ]
        ),
    )


def go_back(page, username, content=None):
    from main import app_shell

    page.clean()
    page.add(
        app_shell(page, username, content) if content else app_shell(page, username)
    )
