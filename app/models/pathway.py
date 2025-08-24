from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Pathway(Base):
    __tablename__ = "pathways"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True)
    name = Column(String(255))
    description = Column(Text)

    product = relationship("Product", back_populates="pathway")
    items = relationship("PathwayItem", back_populates="pathway")


class PathwayItem(Base):
    __tablename__ = "pathway_items"

    id = Column(Integer, primary_key=True, index=True)
    pathway_id = Column(Integer, ForeignKey("pathways.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    order_index = Column(Integer)

    pathway = relationship("Pathway", back_populates="items")
