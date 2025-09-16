
import uuid
from sqlalchemy import UUID, Column, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class InteractiveParagraphModel(Base):
    __tablename__ = "interactive_paragraph"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                unique=True, nullable=False, index=True)
    video_id = Column(UUID(as_uuid=True), ForeignKey("interactive_video.id"))
    view_index = Column(Integer, nullable=False)
    paragraph_text = Column(Text, nullable=False)
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)    
    
    # Relationships
    video = relationship("InteractiveVideoModel", back_populates="paragraphs")
    paragraph_words = relationship("InteractiveWordModel", back_populates="paragraph")
    paragraph_keywords = relationship("InteractiveKeyWordModel", back_populates="paragraph")
    paragraph_visual = relationship("VisualItemModel", back_populates="paragraph", uselist=False)
