# app/models/product.py
import uuid
from datetime import datetime

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from app.core.database import Base
from app.models.rating import ProductRating
from app.models.skill_objective import ProductObjective
from app.models.skill_objective import ProductSkill


class ProductType(Base):
    __tablename__ = "product_types"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,

    )
    name = Column(String(50), unique=True, nullable=False)

    # relationship with products
    products = relationship("Product", back_populates="type")


# ✅ New table for levels
class Level(Base):
    __tablename__ = "levels"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False)
    name = Column(String(50), unique=True, nullable=False)

    # relationship with products
    products = relationship("Product", back_populates="level_obj")


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
    type_id = Column(UUID(as_uuid=True), ForeignKey("product_types.id"), nullable=False, index=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("product_categories.id"), nullable=True, index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    level_id = Column(UUID(as_uuid=True), ForeignKey("levels.id"), nullable=True, index=True)

    # Product fields
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    cover = Column(String(255), nullable=True)
    short_video = Column(String(255), nullable=True)

    language = Column(String(50), nullable=True)
    duration = Column(String(255), nullable=True)

    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    type = relationship("ProductType", back_populates="products")
    category = relationship("ProductCategory", back_populates="products")

    # details
    book_video_detail = relationship("BookVideoDetail", back_populates="product", uselist=False,
                                     cascade="all, delete-orphan")
    book_reading_detail = relationship("BookReadingDetail", back_populates="product", uselist=False,
                                       cascade="all, delete-orphan")
    course_detail = relationship(
        "CourseDetail",
        back_populates="product",
        uselist=False,
        cascade="all, delete-orphan"
    )
    pathway = relationship("Pathway", back_populates="product", uselist=False)
    level_obj = relationship("Level", back_populates="products")

    # user-related relationships
    ratings = relationship("ProductRating", back_populates="product", cascade="all, delete-orphan")
    waiting_list = relationship("UserWaitingList", back_populates="product")
    enrollments = relationship("UserProduct", back_populates="product")

    # ✅ many-to-many via association models
    product_skills = relationship("ProductSkill", back_populates="product", cascade="all, delete")
    product_objectives = relationship("ProductObjective", back_populates="product", cascade="all, delete")

    # ✅ convenience shortcut (viewonly)
    skills = relationship("Skill", secondary="product_skills", viewonly=True)
    objectives = relationship("Objective", secondary="product_objectives", viewonly=True)

    @hybrid_property
    def average_rating(self):
        if not self.ratings:
            return 0.0
        return sum(r.rating for r in self.ratings) / len(self.ratings)

    @average_rating.expression
    def average_rating(cls) -> expression.ColumnElement[float]:  # 👈 type hint
        return (
            select(func.coalesce(func.avg(ProductRating.rating), 0.0))
            .where(ProductRating.product_id == cls.id)
            .correlate_except(ProductRating)
            .scalar_subquery()
        )

    @hybrid_property
    def chapter_count(self):
        if self.course_detail and self.course_detail.chapters:
            return len(self.course_detail.chapters)
        return 0

    @chapter_count.expression
    def chapter_count(cls):
        from app.models.course import CourseDetail, Chapter
        return (
            select(func.count(Chapter.id))
            .join(CourseDetail, Chapter.course_id == CourseDetail.id)
            .where(CourseDetail.product_id == cls.id)
            .correlate_except(Chapter)
            .scalar_subquery()
        )

    @hybrid_property
    def video_count(self):
        if self.course_detail and self.course_detail.chapters:
            return sum(len(ch.videos) for ch in self.course_detail.chapters)
        return 0

    @video_count.expression
    def video_count(cls):
        from app.models.course import CourseDetail, Chapter, Video
        return (
            select(func.count(Video.id))
            .join(Chapter, Video.chapter_id == Chapter.id)
            .join(CourseDetail, Chapter.course_id == CourseDetail.id)
            .where(CourseDetail.product_id == cls.id)
            .correlate_except(Video)
            .scalar_subquery()
        )

    @hybrid_property
    def book_video_count(self):
        if self.book_video_detail and self.book_video_detail.videos:
            return len(self.book_video_detail.videos)
        return 0

    @book_video_count.expression
    def book_video_count(cls):
        from app.models.book import BookVideoDetail, BookVideos
        return (
            select(func.count(BookVideos.id))
            .join(BookVideoDetail, BookVideos.book_id == BookVideoDetail.id)
            .where(BookVideoDetail.product_id == cls.id)
            .correlate_except(BookVideos)
            .scalar_subquery()
        )

    @hybrid_property
    def book_section_count(self):
        if self.book_reading_detail and self.book_reading_detail.sections:
            return len(self.book_reading_detail.sections)
        return 0

    @book_section_count.expression
    def book_section_count(cls):
        from app.models.book import BookReadingDetail, BookSection
        return (
            select(func.count(BookSection.id))
            .join(BookReadingDetail, BookSection.book_id == BookReadingDetail.id)
            .where(BookReadingDetail.product_id == cls.id)
            .correlate_except(BookSection)
            .scalar_subquery()
        )

    @hybrid_property
    def skill_count(self):
        if self.product_skills:
            return len(self.product_skills)
        return 0

    @skill_count.expression
    def skill_count(cls):
        return (
            select(func.count(ProductSkill.id))
            .where(ProductSkill.product_id == cls.id)
            .correlate_except(ProductSkill)
            .scalar_subquery()
        )

    @hybrid_property
    def objective_count(self):
        if self.product_objectives:
            return len(self.product_objectives)
        return 0

    @objective_count.expression
    def objective_count(cls):
        return (
            select(func.count(ProductObjective.id))
            .where(ProductObjective.product_id == cls.id)
            .correlate_except(ProductObjective)
            .scalar_subquery()
        )
