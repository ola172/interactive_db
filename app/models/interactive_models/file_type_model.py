import uuid
from sqlalchemy import Column, String, DateTime, func, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class FileTypeModel(Base):
    __tablename__ = "file_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50), nullable=False, unique=True)  # video, srt, pdf, etc.
    description = Column(Text, nullable=True)
    # allowed_extensions = Column(Text, nullable=True)  # JSON array as text: ["mp4", "avi", "mov"]
    
    # Relationships
    files = relationship("FileModel", back_populates="file_type")

    # metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())