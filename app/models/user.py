import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    profile_image = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    quiz_attempts = relationship("UserQuizAttempt", back_populates="user")
    ratings = relationship("ProductRating", back_populates="user")
    waiting_list = relationship("UserWaitingList", back_populates="user")


class UserProduct(Base):
    __tablename__ = "user_products"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    progress = Column(Integer, default=0)
    status = Column(String(50), default="in_progress")
    is_like = Column(Boolean, default=False)


class UserQuizAttempt(Base):
    __tablename__ = "user_quiz_attempts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"))
    attempt_date = Column(DateTime, default=datetime.utcnow)
    score = Column(Integer)
    passed = Column(Boolean, default=False)

    user = relationship("User", back_populates="quiz_attempts")
    answers = relationship("UserAnswer", back_populates="attempt")


class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    attempt_id = Column(UUID(as_uuid=True), ForeignKey("user_quiz_attempts.id"))
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"))
    answer_id = Column(UUID(as_uuid=True), ForeignKey("answers.id"))
    user_text = Column(Text)
    is_correct = Column(Boolean)

    attempt = relationship("UserQuizAttempt", back_populates="answers")


class UserWaitingList(Base):
    __tablename__ = "user_waiting_list"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="waiting")

    user = relationship("User", back_populates="waiting_list")
    product = relationship("Product", back_populates="waiting_list")
