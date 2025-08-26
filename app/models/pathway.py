import uuid

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Pathway(Base):
    __tablename__ = "pathways"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), unique=True)
    name = Column(String(255))
    description = Column(Text)

    product = relationship("Product", back_populates="pathway")
    items = relationship("PathwayItem", back_populates="pathway")


class PathwayItem(Base):
    __tablename__ = "pathway_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    pathway_id = Column(UUID(as_uuid=True), ForeignKey("pathways.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    order_index = Column(Integer)

    pathway = relationship("Pathway", back_populates="items")
