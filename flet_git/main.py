import random
import flet as ft
from quiz_db import correct_answer_check, get_random_question, get_answers_text
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Create the engine and bind it to your database
engine = create_engine("sqlite:///quiz.db", echo=True)

# Create the tables if they don't exist
# Base.metadata.create_all(engine)

# Create a session
session = Session(engine)


class AnswerButtons(ft.Container):
    def __init__(
            self, 
            options: list, 
            check_func: callable
    ):
        super().__init__()
        
        option_buttons = [
            ft.TextButton(
                content=ft.Container(ft.Text(option), padding=10), 
                on_click=check_func,
                width=400, 
                style=ft.ButtonStyle(
                    side=ft.BorderSide(1, ft.colors.BLUE),
                    bgcolor=ft.colors.WHITE,
                    ),
            )
            for option in options
        ]
        self.content = ft.Column(option_buttons)
        self.alignment = ft.alignment.center
        self.margin = 30


def change_img(e):
    page = e.control.page
    img = page.controls[0].content.controls[0].content
    images = list(range(1, 39))
    rnd = random.choice(images)
    img.src = f"assets/emoji/pngwing.com ({rnd}).png"
    img.visible = True
    page.update()


def check_func(e):
    page = e.control.page
    question_text = page.controls[0].content.controls[1].content.value
    answer_text = e.control.content.content.value
    is_correct = correct_answer_check(question_text, answer_text)

    if is_correct:
        icon = ft.Icon(
            ft.icons.CHECK_CIRCLE_OUTLINED,
            color=ft.colors.GREEN_900,
            size=100
        )
    else:
        icon = ft.Icon(
            ft.icons.HIGHLIGHT_REMOVE,
            color=ft.colors.RED_900,
            size=100
        )

    page.clean()

    def return_page(e):
        page.clean()
        e.control.page = main(page)

    page.add(icon, ft.ElevatedButton('next one', on_click=return_page))
    page.update()


def refresh_func(e):
    page = e.control.page
    img = page.controls[0].content.controls[0].content 
    img.visible = False
    page.update()
    page.clean()

    def return_page(e):
        page.clean()
        e.control.page = main(page)

    page.add(ft.ElevatedButton('button_text', on_click=return_page))


def main(page: ft.Page):
    page.route = "/main"
    answers = (1, 2, 3, 4)
    page.vertical_alignment = "CENTER"
    page.horizontal_alignment = "CENTER"
    question = get_random_question()
    answers = [a.answer for a in get_answers_text(question)]
    random.shuffle(answers)

    img = ft.Image(
        src='assets/emoji/pngwing.com (38).png',
        width=480,
        height=320,
    )
    question_text = ft.Text(
        question.question,
        size=16,
        weight=ft.FontWeight.W_600
    )

    page.add(
        ft.Card(ft.Column(
                [
                    ft.Container(
                        img,
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=20),
                        on_click=change_img
                    ),
                    ft.Container(
                        question_text,
                        alignment=ft.alignment.center,
                        padding=20
                    ),
                    ft.Divider(), 
                    AnswerButtons(answers, check_func),
                ]
            ),
            margin=ft.margin.symmetric(horizontal=20),
            color=ft.colors.BLUE_100,
            width=500,
        ),
    )
    return page

ft.app(main, view=ft.AppView.WEB_BROWSER, assets_dir='.')
