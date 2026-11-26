import flet as ft


def asset_card(name, balance, flag_url):
    return ft.Container(
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


def screen_loader(page, screen_function, username):
    page.clean()
    page.add(screen_function(page, username))
