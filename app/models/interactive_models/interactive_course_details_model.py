import uuid
from sqlalchemy import UUID, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class InteractiveCourseDetailsModel(Base):
    __tablename__ = "interactive_course_details"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), unique=True)
    pre_assessment_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"))
    final_exam_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"))

    # Relationships
    product = relationship("Product", back_populates="course_detail", uselist=False)
    # instructors = relationship("CourseInstructor", back_populates="course")
    chapters = relationship(
        "InteractiveChapterModel",
        back_populates="course",
        order_by="InteractiveChapterModel.view_index",
        cascade="all, delete-orphan",
    )
    product = relationship(
        "Product", back_populates="interactive_course_detail", uselist=False
    )
