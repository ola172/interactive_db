import uuid

from sqlalchemy import Column, String, DateTime, Text, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class AssistFileTypeModel(Base):
    __tablename__ = "assist_file_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50), nullable=False, unique=True)  # video, srt, pdf, etc.
    description = Column(Text, nullable=True)
    # allowed_extensions = Column(Text, nullable=True)  # JSON array as text: ["mp4", "avi", "mov"]
    
    # Relationships
    files = relationship("AssistFileModel", back_populates="file_type")

    # metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AssistFileModel(Base):
    __tablename__ = "assist_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    file_name = Column(String(255), nullable=False)
    video_id = Column(UUID(as_uuid=True), ForeignKey("interactive_video.id"), nullable=True)
    
    # File type relationship
    file_type_id = Column(UUID(as_uuid=True), ForeignKey("assist_file_types.id"), nullable=False)
    
    # Storage information
    bucket_name = Column(String(100), nullable=False)  # specific bucket within storage
    storage_path = Column(String(500), nullable=False)   # full path to file
    file_url = Column(String(1000), nullable=True)       # public URL if available

    # Relationships
    file_type = relationship("AssistFileTypeModel", back_populates="files")
    images = relationship("AssistImageModel", back_populates="file", cascade="all, delete-orphan")
    video = relationship("InteractiveVideoModel", back_populates="files")

    # metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
