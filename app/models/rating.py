from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class ProductRating(Base):
    __tablename__ = "product_ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    rating = Column(Integer)
    review = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint("user_id", "product_id", name="uq_user_product_rating"),)

    user = relationship("User", back_populates="ratings")
    product = relationship("Product", back_populates="ratings")
