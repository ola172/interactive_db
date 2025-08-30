# app/models/product.py
import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class ProductType(Base):
    __tablename__ = "product_types"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )
    name = Column(String(50), unique=True, nullable=False)

    # relationship with products
    products = relationship("Product", back_populates="type")


class Product(Base):
    __tablename__ = "products"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )

    # Foreign keys
    type_id = Column(UUID(as_uuid=True), ForeignKey("product_types.id"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("product_categories.id"), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # Product fields
    price = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    cover = Column(String(255), nullable=True)
    short_video = Column(String(255), nullable=True)

    language = Column(String(50), nullable=True)
    level = Column(String(50), nullable=True)
    duration = Column(Integer, nullable=True)

    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    type = relationship("ProductType", back_populates="products")
    category = relationship("ProductCategory", back_populates="products")

    # details
    book_video_detail = relationship("BookVideoDetail", back_populates="product", uselist=False)
    book_reading_detail = relationship("BookReadingDetail", back_populates="product", uselist=False)
    course_detail = relationship(
        "CourseDetail",
        back_populates="product",
        uselist=False,
        cascade="all, delete-orphan"
    )
    pathway = relationship("Pathway", back_populates="product", uselist=False)

    # user-related relationships
    ratings = relationship("ProductRating", back_populates="product")
    waiting_list = relationship("UserWaitingList", back_populates="product")
    enrollments = relationship("UserProduct", back_populates="product")

    # ✅ many-to-many via association models
    product_skills = relationship("ProductSkill", back_populates="product", cascade="all, delete")
    product_objectives = relationship("ProductObjective", back_populates="product", cascade="all, delete")

    # ✅ convenience shortcut (viewonly)
    skills = relationship("Skill", secondary="product_skills", viewonly=True)
    objectives = relationship("Objective", secondary="product_objectives", viewonly=True)


