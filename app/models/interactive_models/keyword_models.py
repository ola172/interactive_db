

import uuid
from sqlalchemy import UUID, Column, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class InteractiveKeyWordModel(Base):
    __tablename__ = "interactive_paragraph_keywords"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                unique=True, nullable=False, index=True)
    paragraph_id = Column(UUID(as_uuid=True), ForeignKey("interactive_paragraph.id"))
    type_id = Column(UUID(as_uuid=True), ForeignKey("interactive_keyword_type.id"))
    word = Column(Text, nullable=False)
    
    # Relationships
    paragraph = relationship("InteractiveParagraphModel", back_populates="paragraph_keywords")
    type = relationship("KeyWordTypeModel", back_populates="keywords")


class KeyWordTypeModel(Base):
    __tablename__ = "interactive_keyword_type"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
            unique=True, nullable=False, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    # Relationships
    keywords = relationship("InteractiveKeyWordModel", back_populates="type")
    video_styles = relationship("VideoKeywordTypeStyleModel", back_populates="type", foreign_keys="VideoKeywordTypeStyleModel.keyword_type_id")



class VideoKeywordTypeStyleModel(Base):
    __tablename__ = "video_keyword_type_style"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    video_id = Column(UUID(as_uuid=True), ForeignKey("interactive_video.id"))
    keyword_type_id = Column(UUID(as_uuid=True), ForeignKey("interactive_keyword_type.id"))

    # Style properties (per video × type)
    color_light = Column(Text, nullable=False)
    color_dark = Column(Text, nullable=False)
    shadow_light = Column(Text, nullable=True)
    shadow_dark = Column(Text, nullable=True)
    size = Column(Integer, nullable=False, default=14)

    video = relationship("InteractiveVideoModel", back_populates="type_styles")
    type = relationship("KeyWordTypeModel", back_populates="video_styles", foreign_keys=[keyword_type_id]
)
