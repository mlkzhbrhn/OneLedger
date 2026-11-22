import flet as ft


def main(page: ft.Page):
    page.title = "OneLedger"
    page.appbar = ft.AppBar(title=ft.Text("OneLedger"), center_title=True)

    page.add(
        ft.Column(
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
                        ft.Text("0 PKR"),
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Button("+"),
                                        ft.Text("Deposit"),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Column(
                                    [
                                        ft.Button("-"),
                                        ft.Text("Withdraw"),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Column(
                                    [
                                        ft.Button("->"),
                                        ft.Text("Transfer"),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Column(
                                    [
                                        ft.Button("x"),
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
            ]
        )
    )


if __name__ == "__main__":
    ft.run(main)
