from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, func
from models import Question, Answer
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///quiz.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def correct_answer_check(question_text: str, answer_text: str):
    question_id = session.scalars(
        select(Question.id)
        .where(Question.question == question_text)
    ).first()
    correct_answer_text = session.scalars(
        select(Answer.answer)
        .join(Question.answers)
        .where(
            (Answer.question_id == question_id) & (Answer.is_correct == True)
        )
    ).first()
    return answer_text == correct_answer_text
    

def get_random_question() -> Question:
    question = session.scalars(select(Question)
                               .order_by(func.random())
                               .limit(1)).one()
    return question


def get_question_text(question: Question) -> str:
    return question.question


def get_answers_text(question: Question) -> list:
    return question.answers
