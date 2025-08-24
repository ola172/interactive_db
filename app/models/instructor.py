from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.core.database import Base


class Instructor(Base):
    __tablename__ = "instructors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    title = Column(String(255))
    bio = Column(Text)
    linkedin = Column(String(255))
    education = Column(Text)
    profile_image = Column(String(255))

    rating = Column(DECIMAL(2, 1))
    review_count = Column(Integer, default=0)
    courses_count = Column(Integer, default=0)
    students_count = Column(Integer, default=0)

    is_top_rated = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    is_expert = Column(Boolean, default=False)
    is_new = Column(Boolean, default=False)

    # relationships
    skills = relationship("InstructorSkill", back_populates="instructor")
    course_links = relationship("CourseInstructor", back_populates="instructor")


class InstructorSkill(Base):
    __tablename__ = "instructor_skills"

    id = Column(Integer, primary_key=True, index=True)
    instructor_id = Column(Integer, ForeignKey("instructors.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))

    instructor = relationship("Instructor", back_populates="skills")
    skill = relationship("Skill", back_populates="instructors")
