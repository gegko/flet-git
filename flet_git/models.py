from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    telegram_username = Column(String(30))


class Question(Base):
    __tablename__ = "question"
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answers = relationship("Answer", back_populates="question")


class Answer(Base):
    __tablename__ = "answer"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id'))
    answer = Column(String)
    is_correct = Column(Boolean)
    question = relationship("Question", back_populates="answers")
