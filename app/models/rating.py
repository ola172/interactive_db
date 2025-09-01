import uuid
from datetime import datetime
from statistics import mean

from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class ProductRating(Base):
    __tablename__ = "product_ratings"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer)
    review = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint("user_id", "product_id", name="uq_user_product_rating"),)

    # ✅ Correct relationships
    user = relationship("User", back_populates="ratings")
    product = relationship("Product", back_populates="ratings")

    @property
    def average_rating(self) -> float:
        if not self.product or not self.product.ratings:
            return 0.0
        return round(mean(r.rating for r in self.product.ratings), 2)
