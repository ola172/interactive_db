# app/models/product_category.py
import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    # all products in this category
    products = relationship("Product", back_populates="category")
