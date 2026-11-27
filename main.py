import flet as ft

import auth
from ui_crypto_view import crypto_screen
from ui_earn_view import earn_screen
from ui_fiat_view import dashboard
from ui_loans_view import loans_screen


def authentication(page):
    username_field = ft.TextField(width=200)
    password_field = ft.TextField(password=True, width=200, can_reveal_password=True)
    status_message = ft.Text("", color=ft.Colors.RED)

    def handle_login():
        username = username_field.value
        password = password_field.value

        if not username:
            status_message.value = "Please enter username"
        elif not password:
            status_message.value = "Please enter password"
        else:
            status_message.value = ""
            result = auth.login_user(username, password)
            if not result:
                status_message.value = "Invalid username or password"
            else:
                status_message.value = ""
                page.clean()
                page.add(dashboard(page, username))

    def handle_register():
        username = username_field.value
        password = password_field.value

        if not username:
            status_message.value = "Please enter username"
        elif not password:
            status_message.value = "Please enter password"
        else:
            status_message.value = ""
            result = auth.register_user(username, password, role="user")
            if not result:
                status_message.value = "Error registering user. Please try again."
            else:
                status_message.value = "Registration successful. Please login."

    return ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Username", width=70),
                        username_field,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Text("Password", width=70),
                        password_field,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [status_message],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Button("Login", on_click=handle_login),
                        ft.Button("Register", on_click=handle_register),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        ),
        expand=True,
    )


def app_shell(page, username, content=dashboard):
    content_area = ft.Container(content=content(page, username), expand=True)

    def switch_view(view_fn):
        content_area.content = view_fn(page, username)

    sidebar = ft.Container(
        width=160,
        padding=12,
        content=ft.Column(
            [
                ft.Button("Dashboard", on_click=lambda: switch_view(dashboard)),
                ft.Button("Crypto", on_click=lambda: switch_view(crypto_screen)),
                ft.Button("Loans", on_click=lambda: switch_view(loans_screen)),
                ft.Button("Earn", on_click=lambda: switch_view(earn_screen)),
            ],
            spacing=10,
        ),
    )

    return ft.Row([sidebar, content_area], expand=True, spacing=0)


def main(page: ft.Page):
    page.title = "OneLedger"
    page.appbar = ft.AppBar(
        title=ft.Text("OneLedger"),
        center_title=True,
    )

    page.add(app_shell(page, "jeff"))


if __name__ == "__main__":
    ft.run(main)
