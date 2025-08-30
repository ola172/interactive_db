import uuid

from sqlalchemy import Column, String, Text, ForeignKey, UniqueConstraint
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
        index=True,
    )
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    instructors = relationship("InstructorSkill", back_populates="skill", cascade="all, delete")
    product_skills = relationship("ProductSkill", back_populates="skill", cascade="all, delete")


class ProductSkill(Base):
    __tablename__ = "product_skills"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=False)

    __table_args__ = (UniqueConstraint("product_id", "skill_id", name="uq_product_skill"),)

    # Relationships
    product = relationship("Product", back_populates="product_skills")
    skill = relationship("Skill", back_populates="product_skills")


class Objective(Base):
    __tablename__ = "objectives"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    product_objectives = relationship("ProductObjective", back_populates="objective", cascade="all, delete")


class ProductObjective(Base):
    __tablename__ = "product_objectives"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    objective_id = Column(UUID(as_uuid=True), ForeignKey("objectives.id"), nullable=False)

    __table_args__ = (UniqueConstraint("product_id", "objective_id", name="uq_product_objective"),)

    # Relationships
    product = relationship("Product", back_populates="product_objectives")
    objective = relationship("Objective", back_populates="product_objectives")
