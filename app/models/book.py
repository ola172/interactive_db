import uuid

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class BookVideoDetail(Base):
    __tablename__ = "book_video_details"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), unique=True)
    author_name = Column(String(255))
    total_videos = Column(Integer)
    total_hours = Column(Integer)
    url = Column(String(255))

    product = relationship("Product", back_populates="book_video_detail")


class BookReadingDetail(Base):
    __tablename__ = "book_reading_details"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), unique=True)
    author_name = Column(String(255))
    author_bio = Column(Text)
    page_count = Column(Integer)
    reading_time = Column(Integer)
    readers_count = Column(Integer)
    is_new = Column(Boolean, default=False)

    product = relationship("Product", back_populates="book_reading_detail")
    sections = relationship("BookSection", back_populates="book")


class BookSection(Base):
    __tablename__ = "book_sections"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    book_id = Column(UUID(as_uuid=True), ForeignKey("book_reading_details.id"))
    title = Column(String(255))
    content = Column(Text)
    stage_index = Column(Integer)

    book = relationship("BookReadingDetail", back_populates="sections")
