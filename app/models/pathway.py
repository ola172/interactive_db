import uuid
from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Pathway(Base):
    __tablename__ = "pathways"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        index=True
    )

    # each pathway corresponds to a product
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    name = Column(String(255), nullable=False)
    description = Column(Text)

    # relationships
    product = relationship("Product", back_populates="pathway", uselist=False)
    items = relationship("PathwayItem", back_populates="pathway", cascade="all, delete-orphan")


class PathwayItem(Base):
    __tablename__ = "pathway_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        index=True
    )

    pathway_id = Column(
        UUID(as_uuid=True),
        ForeignKey("pathways.id", ondelete="CASCADE"),
        nullable=False
    )
    product_id = Column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )

    order_index = Column(Integer, nullable=False)

    # prevent duplicate product in same pathway
    __table_args__ = (
        UniqueConstraint("pathway_id", "product_id", name="uq_pathway_product"),
    )

    # relationships
    pathway = relationship("Pathway", back_populates="items")
    product = relationship("Product")
