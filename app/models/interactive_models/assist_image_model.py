import enum
import uuid

from sqlalchemy import Boolean, Column, ForeignKey, DateTime, func, Enum, Text, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base
        

class AssistImageTypeEnum(str, enum.Enum):
    IMAGE = "image"
    CHART = "chart"
    TABLE = "table"


class AssistImageModel(Base):
    __tablename__ = "assist_images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    file_id = Column(UUID(as_uuid=True), ForeignKey("assist_files.id", ondelete="CASCADE"), nullable=False)
    visual_item_id = Column(UUID(as_uuid=True), ForeignKey("visual_items.id"), nullable=True)

    # Image information
    image_title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    proposed_image_type = Column(Enum(AssistImageTypeEnum), nullable=False)
    is_protected = Column(Boolean, nullable=False, default=False)
    
    # Storage information
    original_image_url = Column(String(1000), nullable=False)
    searched_image_url = Column(String(1000), nullable=True)
    image_3d_url = Column(String(1000), nullable= True)
    bucket_name = Column(String(100), nullable=True)  # storage bucket
    storage_path = Column(String(500), nullable=True)  # path in storage
        
    # Relationships
    file = relationship("AssistFileModel", back_populates="images")
    visual_item = relationship("VisualItemModel", back_populates="assist_image")
    # metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
   

