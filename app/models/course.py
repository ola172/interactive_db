import uuid

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class CourseDetail(Base):
    __tablename__ = "course_details"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), unique=True)

    # schema fields
    video_count = Column(Integer)
    total_hours = Column(Integer)
    students_count = Column(Integer)
    pre_assessment_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"))
    final_exam_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"))
    certificate_included = Column(Boolean, default=False)

    # additional fields
    view_index = Column(Integer, nullable=True)
    about = Column(Text, nullable=True)
    duration = Column(String(20), nullable=True)

    # Relationships
    product = relationship("Product", back_populates="course_detail", uselist=False)
    instructors = relationship("CourseInstructor", back_populates="course")
    chapters = relationship(
        "Chapter",
        back_populates="course",
        order_by="Chapter.view_index",
        cascade="all, delete-orphan"
    )


class CourseInstructor(Base):
    __tablename__ = "course_instructors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                unique=True, nullable=False, index=True)
    course_id = Column(UUID(as_uuid=True), ForeignKey("course_details.id"))
    instructor_id = Column(UUID(as_uuid=True), ForeignKey("instructors.id"))

    course = relationship("CourseDetail", back_populates="instructors")
    instructor = relationship("Instructor", back_populates="course_links")


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                unique=True, nullable=False, index=True)
    course_id = Column(UUID(as_uuid=True), ForeignKey("course_details.id"))
    title = Column(String(255))
    description = Column(Text)
    view_index = Column(Integer, nullable=True)
    about = Column(Text, nullable=True)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"))

    course = relationship("CourseDetail", back_populates="chapters")
    videos = relationship(
        "Video",
        back_populates="chapter",
        order_by="Video.view_index",
        cascade="all, delete-orphan"
    )


class Video(Base):
    __tablename__ = "videos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                unique=True, nullable=False, index=True)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"))
    title = Column(String(255))  # JSON "videoName"
    url = Column(String(255))
    video_duration = Column(String(20), nullable=True)
    view_index = Column(Integer, nullable=True)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"))

    chapter = relationship("Chapter", back_populates="videos")
