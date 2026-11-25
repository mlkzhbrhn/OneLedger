import asyncio

import flet as ft

import auth
import conversion
import deposit
import persistence
import transfer
import withdrawal


def transfer_screen(page, username):
    recipient_field = ft.TextField(label="Recipient", width=150)
    amount_field = ft.TextField(label="Amount", width=150)
    currency_field = ft.Dropdown(
        label="Currency",
        options=[
            ft.dropdown.Option("PKR"),
            ft.dropdown.Option("USD"),
        ],
        width=150,
    )
    status_message = ft.Text("", color=ft.Colors.RED)

    def go_back():
        page.clean()
        page.add(dashboard(page, username))

    def handle_transfer():
        recipient = recipient_field.value.strip()
        currency = currency_field.value

        if not recipient:
            status_message.value = "Please enter recipient username"
            return
        if not currency:
            status_message.value = "Please select currency"
            return

        try:
            amount = float(amount_field.value)
        except ValueError:
            status_message.value = "Please enter a valid amount"
            return

        if amount <= 0:
            status_message.value = "Amount must be greater than zero"
            return

        result = transfer.transfer_funds(username, recipient, amount, currency)
        if not result:
            status_message.value = "Transfer failed. Check recipient or balance."
        else:
            go_back()

    return ft.Container(
        ft.Column(
            [
                ft.Row(
                    [ft.Text("Recipient", width=70), recipient_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [ft.Text("Currency", width=70), currency_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [ft.Text("Amount", width=70), amount_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [status_message],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Button("Transfer", on_click=handle_transfer),
                        ft.Button("Cancel", on_click=go_back),
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


def withdrawal_screen(page, username):
    amount_field = ft.TextField(label="Amount", width=150)
    currency_field = ft.Dropdown(
        label="Currency",
        options=[
            ft.dropdown.Option("PKR"),
            ft.dropdown.Option("USD"),
        ],
        width=150,
    )
    status_message = ft.Text("", color=ft.Colors.RED)

    def go_back():
        page.clean()
        page.add(dashboard(page, username))

    def handle_withdrawal():
        currency = currency_field.value
        try:
            amount = float(amount_field.value)
        except ValueError:
            status_message.value = "Please enter a valid amount"
            return

        if not amount:
            status_message.value = "Please enter amount"
        elif not currency:
            status_message.value = "Please select currency"

        result = withdrawal.withdrawal(username, amount, currency)
        if not result:
            status_message.value = "Error withdrawing funds. Please try again."
        else:
            status_message.value = "Withdrawal successful."
            go_back()

    withdrawal_page = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [ft.Text("Currency", width=70), currency_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [ft.Text("Amount", width=70), amount_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [status_message],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Button("Withdraw", on_click=handle_withdrawal),
                        ft.Button("Cancel", on_click=go_back),
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

    return withdrawal_page


def deposit_screen(page, username):
    amount_field = ft.TextField(label="Amount", width=150)
    currency_field = ft.Dropdown(
        label="Currency",
        options=[
            ft.dropdown.Option("PKR"),
            ft.dropdown.Option("USD"),
        ],
        width=150,
    )
    status_message = ft.Text("", color=ft.Colors.RED)

    def go_back():
        page.clean()
        page.add(dashboard(page, username))

    def handle_deposit():
        currency = currency_field.value
        try:
            amount = float(amount_field.value)
        except ValueError:
            status_message.value = "Please enter a valid amount"
            return

        if not amount:
            status_message.value = "Please enter amount"
        elif not currency:
            status_message.value = "Please select currency"

        result = deposit.deposit(username, amount, currency)
        if not result:
            status_message.value = "Error depositing funds. Please try again."
        else:
            status_message.value = "Deposit successful."
            go_back()

    deposit_page = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [ft.Text("Currency", width=70), currency_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [ft.Text("Amount", width=70), amount_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [status_message],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Button("Deposit", on_click=handle_deposit),
                        ft.Button("Cancel", on_click=go_back),
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

    return deposit_page


def convert_screen(page, username):
    fiat_currency_field = ft.Dropdown(
        label="From (Fiat)",
        options=[
            ft.dropdown.Option("PKR"),
            ft.dropdown.Option("USD"),
        ],
        width=150,
    )
    crypto_currency_field = ft.Dropdown(
        label="To (Crypto)",
        options=[
            ft.dropdown.Option("BTC"),
            ft.dropdown.Option("ETH"),
        ],
        width=150,
    )
    amount_field = ft.TextField(label="Fiat Amount", width=150)
    status_message = ft.Text("", color=ft.Colors.RED)
    loader = ft.ProgressRing(visible=False, width=50, height=50)

    def go_back():
        page.clean()
        page.add(dashboard(page, username))

    async def handle_convert():
        fiat_currency = fiat_currency_field.value
        crypto_currency = crypto_currency_field.value

        if not fiat_currency:
            status_message.value = "Please select fiat currency"
            return
        if not crypto_currency:
            status_message.value = "Please select crypto asset"
            return

        try:
            amount = float(amount_field.value)
        except ValueError:
            status_message.value = "Please enter a valid amount"
            return

        if amount <= 0:
            status_message.value = "Amount must be greater than zero"
            return

        loader.visible = True
        status_message.value = "Converting..."
        page.update()

        result = await asyncio.to_thread(
            conversion.convert_fiat_to_crypto,
            username,
            amount,
            fiat_currency,
            crypto_currency,
        )

        loader.visible = False

        if not result:
            status_message.value = "Conversion failed. Check balance or exchange rates."
        else:
            go_back()

    return ft.Container(
        ft.Column(
            [
                ft.Row(
                    [ft.Text("From", width=70), fiat_currency_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [ft.Text("To", width=70), crypto_currency_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [ft.Text("Amount", width=70), amount_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [loader, status_message],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Button("Convert", on_click=handle_convert),
                        ft.Button("Cancel", on_click=go_back),
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


def dashboard(page, username):
    db = persistence.load_db()
    user = db[username]
    fiat_txs = user["fiat"]["transactions"]
    pkr_balance = user["fiat"]["balances"]["PKR"]

    def deposit_screen_loader():
        page.clean()
        page.add(deposit_screen(page, username))

    def withdrawal_screen_loader():
        page.clean()
        page.add(withdrawal_screen(page, username))

    def transfer_screen_loader():
        page.clean()
        page.add(transfer_screen(page, username))

    def convert_screen_loader():
        page.clean()
        page.add(convert_screen(page, username))

    return ft.Column(
        [
            ft.Row(
                [
                    ft.CircleAvatar(
                        foreground_image_src="https://flagcdn.com/w80/pk.png",
                        radius=24,
                    ),
                    ft.Text("PKR balance"),
                ]
            ),
            ft.Row(
                [
                    ft.Text(f"{pkr_balance} PKR"),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Button("+", on_click=deposit_screen_loader),
                                    ft.Text("Deposit"),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Column(
                                [
                                    ft.Button("-", on_click=withdrawal_screen_loader),
                                    ft.Text("Withdraw"),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Column(
                                [
                                    ft.Button("->", on_click=transfer_screen_loader),
                                    ft.Text("Transfer"),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Column(
                                [
                                    ft.Button("x", on_click=convert_screen_loader),
                                    ft.Text("Convert"),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ]
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(),
            ft.Column(
                [
                    ft.Text("Transactions"),
                    ft.Column(
                        [
                            *(
                                ft.Text(
                                    f"{fiat_txs[i]['type']} {fiat_txs[i]['amount']} {fiat_txs[i]['currency']} on {fiat_txs[i]['date']}"
                                )
                                for i in range(len(fiat_txs))
                            )
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                ]
            ),
        ]
    )


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


def main(page: ft.Page):
    page.title = "OneLedger"
    page.appbar = ft.AppBar(title=ft.Text("OneLedger"), center_title=True)

    page.add(authentication(page))


if __name__ == "__main__":
    ft.run(main)
