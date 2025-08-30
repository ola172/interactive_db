import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Float, UniqueConstraint, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class UserRole(enum.Enum):
    student = "student"
    instructor = "instructor"
    admin = "admin"


class EnrollmentStatus(enum.Enum):
    in_progress = "in_progress"
    completed = "completed"
    dropped = "dropped"


class WaitingStatus(enum.Enum):
    waiting = "waiting"
    notified = "notified"
    enrolled = "enrolled"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    profile_image = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.student)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_login_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    quiz_attempts = relationship("UserQuizAttempt", back_populates="user")
    ratings = relationship("ProductRating", back_populates="user")
    waiting_list = relationship("UserWaitingList", back_populates="user")
    enrollments = relationship("UserProduct", back_populates="user")


class UserProduct(Base):
    __tablename__ = "user_products"
    __table_args__ = (UniqueConstraint("user_id", "product_id", name="uq_user_product"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    progress = Column(Float, default=0.0)
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.in_progress)
    is_like = Column(Boolean, default=False)

    user = relationship("User", back_populates="enrollments")
    product = relationship("Product", back_populates="enrollments")



class UserQuizAttempt(Base):
    __tablename__ = "user_quiz_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"), nullable=False)
    attempt_date = Column(DateTime, default=datetime.utcnow)
    score = Column(Float)  # allow decimals
    duration_seconds = Column(Integer)  # optional: track time taken
    passed = Column(Boolean, default=False)

    user = relationship("User", back_populates="quiz_attempts")
    answers = relationship("UserAnswer", back_populates="attempt")


class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    attempt_id = Column(UUID(as_uuid=True), ForeignKey("user_quiz_attempts.id"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    answer_id = Column(UUID(as_uuid=True), ForeignKey("answers.id"))
    user_text = Column(Text)
    is_correct = Column(Boolean)
    answered_at = Column(DateTime, default=datetime.utcnow)

    attempt = relationship("UserQuizAttempt", back_populates="answers")


class UserWaitingList(Base):
    __tablename__ = "user_waiting_list"
    __table_args__ = (UniqueConstraint("user_id", "product_id", name="uq_user_waiting"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(WaitingStatus), default=WaitingStatus.waiting)

    user = relationship("User", back_populates="waiting_list")
    product = relationship("Product", back_populates="waiting_list")
