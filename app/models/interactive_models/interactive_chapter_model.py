

import uuid
from sqlalchemy import UUID, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class InteractiveChapterModel(Base):
    __tablename__ = "interactive_chapter"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                unique=True, nullable=False, index=True)
    course_id = Column(UUID(as_uuid=True), ForeignKey("interactive_course_details.id"))
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"))
    title = Column(Text, nullable=False)
    description = Column(Text)
    about = Column(Text, nullable=True)
    view_index = Column(Integer, nullable=False)

    # Relationships
    course = relationship("InteractiveCourseDetailsModel", back_populates="chapters")
    videos = relationship(
        "InteractiveVideoModel",
        back_populates="chapter",
        order_by="InteractiveVideoModel.view_index",
        cascade="all, delete-orphan"
    )
