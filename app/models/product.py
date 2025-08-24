# app/models/product.py
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class ProductType(Base):
    __tablename__ = "product_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    # relationship with products
    products = relationship("Product", back_populates="type")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("product_types.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    language = Column(String(50), nullable=True)
    level = Column(String(50), nullable=True)
    duration = Column(Integer, nullable=True)  # duration in minutes
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship with product type
    type = relationship("ProductType", back_populates="products")

    # relationships with books
    book_video_detail = relationship("BookVideoDetail", back_populates="product", uselist=False)
    book_reading_detail = relationship("BookReadingDetail", back_populates="product", uselist=False)

    # relationship with courses
    course_detail = relationship("CourseDetail", back_populates="product", uselist=False)

    pathway = relationship("Pathway", back_populates="product", uselist=False)
    ratings = relationship("ProductRating", back_populates="product")
    product_skills = relationship("ProductSkill", back_populates="product")
    waiting_list = relationship("UserWaitingList", back_populates="product")
