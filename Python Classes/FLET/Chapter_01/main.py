import flet as ft
import random

colors = ["red", "green", "blue", "yellow", "orange", "purple"]

def main(page: ft.Page):
    page.title = "Hello World!"

    # Create named controls
    header_text = ft.Text("Hello World! This is my first FLET app!")
    name_field = ft.TextField(label="Your Name")

    # Define button handler
    def submit_clicked(e):
        if not name_field.value:
            header_text.value = "Rats, you forgot to enter a name. Please enter your name."
        else:
            header_text.value = f"Hello, {name_field.value}. What a lovely name!"
            header_text.color = random.choice(colors)
        page.update()

    submit_button = ft.ElevatedButton("Submit",on_click=submit_clicked, icon=ft.Icons.SEND)

    # Add controls to the page
    page.add(header_text, name_field, submit_button)
    page.controls.append(ft.Text("This is a new line added to the page.", color="red"))
    page.update()

ft.run(main, view=ft.AppView.WEB_BROWSER)