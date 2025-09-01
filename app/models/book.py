import uuid

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class BookVideoDetail(Base):
    __tablename__ = "book_video_details"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), unique=True)

    author_name = Column(String(255))
    expected_time_completion = Column(Integer, nullable=True)

    # Relationships
    product = relationship("Product", back_populates="book_video_detail")
    videos = relationship("BookVideos", back_populates="book", cascade="all, delete-orphan")


class BookVideos(Base):
    __tablename__ = "book_videos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    book_id = Column(UUID(as_uuid=True), ForeignKey("book_video_details.id"))

    video_name = Column(String(255))
    video_duration = Column(String(50))
    url = Column(String(255))
    view_index = Column(Integer)

    # Relationship
    book = relationship("BookVideoDetail", back_populates="videos")


##############################################################
class BookReadingDetail(Base):
    __tablename__ = "book_reading_details"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), unique=True)

    author_name = Column(String(255))
    author_bio = Column(Text)
    page_count = Column(Integer)
    reading_time = Column(Integer)
    is_new = Column(Boolean, default=False)

    product = relationship("Product", back_populates="book_reading_detail")
    sections = relationship("BookSection", back_populates="book")


class BookSection(Base):
    __tablename__ = "book_sections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    book_id = Column(UUID(as_uuid=True), ForeignKey("book_reading_details.id"))

    title = Column(String(255))
    content = Column(Text)
    stage_index = Column(Integer)

    book = relationship("BookReadingDetail", back_populates="sections")
