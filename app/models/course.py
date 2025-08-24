from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class CourseDetail(Base):
    __tablename__ = "course_details"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True)
    video_count = Column(Integer)
    total_hours = Column(Integer)
    students_count = Column(Integer)
    pre_assessment_id = Column(Integer, ForeignKey("quizzes.id"))
    final_exam_id = Column(Integer, ForeignKey("quizzes.id"))
    certificate_included = Column(Boolean, default=False)

    # One-to-one relationship with Product
    product = relationship("Product", back_populates="course_detail", uselist=False)

    # One-to-many relationships
    instructors = relationship("CourseInstructor", back_populates="course")
    chapters = relationship("Chapter", back_populates="course")


class CourseInstructor(Base):
    __tablename__ = "course_instructors"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("course_details.id"))
    instructor_id = Column(Integer, ForeignKey("instructors.id"))

    course = relationship("CourseDetail", back_populates="instructors")
    instructor = relationship("Instructor", back_populates="course_links")


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("course_details.id"))
    title = Column(String(255))
    description = Column(Text)
    order_index = Column(Integer)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))

    course = relationship("CourseDetail", back_populates="chapters")
    videos = relationship("Video", back_populates="chapter")


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    title = Column(String(255))
    url = Column(String(255))
    duration = Column(Integer)
    order_index = Column(Integer)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))

    chapter = relationship("Chapter", back_populates="videos")
