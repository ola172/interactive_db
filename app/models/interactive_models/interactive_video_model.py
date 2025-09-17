import uuid
from sqlalchemy import UUID, Column, ForeignKey, Integer, Interval, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class InteractiveVideoModel(Base):
    __tablename__ = "interactive_video"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("interactive_chapter.id"))
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"))
    title = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    video_duration = Column(Interval, nullable=False)
    view_index = Column(Integer, nullable=False)

    # Relationships
    chapter = relationship("InteractiveChapterModel", back_populates="videos")
    paragraphs = relationship(
        "InteractiveParagraphModel",
        back_populates="video",
        order_by="InteractiveParagraphModel.view_index",
        cascade="all, delete-orphan",
    )
    type_styles = relationship("VideoKeywordTypeStyleModel", back_populates="video")
