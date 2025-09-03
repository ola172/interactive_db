import uuid
from datetime import datetime
from statistics import mean

from sqlalchemy import Column, Text, ForeignKey, DateTime, UniqueConstraint, Float
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Instructor(Base):
    __tablename__ = "instructors"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    name = Column(String(255), nullable=False)
    title = Column(String(255))
    bio = Column(Text)
    linkedin = Column(String(255))
    education = Column(Text)
    profile_image = Column(String(255))

    is_top_rated = Column(Boolean, default=False)
    is_new = Column(Boolean, default=False)

    # relationships
    skills = relationship("InstructorSkill", back_populates="instructor")
    course_links = relationship("CourseInstructor", back_populates="instructor")
    ratings = relationship(
        "InstructorRating",
        back_populates="instructor",
        cascade="all, delete-orphan"
    )


class InstructorSkill(Base):
    __tablename__ = "instructor_skills"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    instructor_id = Column(UUID(as_uuid=True), ForeignKey("instructors.id"))
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"))

    instructor = relationship("Instructor", back_populates="skills")
    skill = relationship("Skill", back_populates="instructors")


class InstructorRating(Base):
    __tablename__ = "instructor_ratings"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    instructor_id = Column(UUID(as_uuid=True), ForeignKey("instructors.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Float, nullable=False)
    review = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint("user_id", "instructor_id", name="uq_user_instructor_rating"),)

    # Relationships
    user = relationship("User", back_populates="instructor_ratings")
    instructor = relationship("Instructor", back_populates="ratings")

    @property
    def average_rating(self) -> float:
        if not self.instructor or not self.instructor.ratings:
            return 0.0
        return round(mean(r.rating for r in self.instructor.ratings), 2)
