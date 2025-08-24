from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    passing_score = Column(Integer)

    questions = relationship("QuizQuestion", back_populates="quiz")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text)
    question_type = Column(String(50))
    difficulty = Column(String(50))

    answers = relationship("Answer", back_populates="question")
    quiz_links = relationship("QuizQuestion", back_populates="question")


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    quiz_id = Column(Integer, ForeignKey("quizzes.id"), primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"), primary_key=True)
    order_index = Column(Integer)

    quiz = relationship("Quiz", back_populates="questions")
    question = relationship("Question", back_populates="quiz_links")


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer_text = Column(Text)
    is_correct = Column(Boolean)

    question = relationship("Question", back_populates="answers")
