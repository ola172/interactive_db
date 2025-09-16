

import uuid
from sqlalchemy import UUID, Column, Float, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class InteractiveWordModel(Base):
    __tablename__ = "interactive_paragraph_words"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                unique=True, nullable=False, index=True)
    paragraph_id = Column(UUID(as_uuid=True), ForeignKey("interactive_paragraph.id"))
    type_id = Column(UUID(as_uuid=True), ForeignKey("interactive_word_type.id"))
    word = Column(Text, nullable=False)
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)    
    
    # Relationships
    paragraph = relationship("InteractiveParagraphModel", back_populates="paragraph_words")
    type = relationship("WordTypeModel", back_populates="words")


class WordTypeModel(Base):
    __tablename__ = "interactive_word_type"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
            unique=True, nullable=False, index=True)
    name = Column(Text, nullable=False)

    # Relationships
    words = relationship("InteractiveWordModel", back_populates="type")
