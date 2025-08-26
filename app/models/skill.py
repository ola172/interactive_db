import uuid

from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)

    instructors = relationship("InstructorSkill", back_populates="skill")
    product_skills = relationship("ProductSkill", back_populates="skill")


class ProductSkill(Base):
    __tablename__ = "product_skills"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"))

    __table_args__ = (UniqueConstraint("product_id", "skill_id", name="uq_product_skill"),)

    product = relationship("Product", back_populates="product_skills")
    skill = relationship("Skill", back_populates="product_skills")
