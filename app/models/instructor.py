import uuid

from sqlalchemy import Column, String, Text, Boolean, ForeignKey
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
