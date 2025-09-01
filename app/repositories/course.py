from typing import Sequence, Any, Coroutine
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Product, ProductSkill, ProductRating
from app.models.course import CourseDetail, Chapter, Video, CourseInstructor
from app.models.skill_objective import ProductObjective
from app.repositories.base_repo import BaseRepository


class CourseDetailRepository(BaseRepository[CourseDetail]):
    def __init__(self, db: AsyncSession, ):
        super().__init__(CourseDetail, db)

    async def get_by_product_id_(self, product_id: UUID) -> CourseDetail | None:
        stmt = select(CourseDetail).where(CourseDetail.product_id == product_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_course_product(self, product_id: UUID) -> Product | None:
        stmt = (
            select(Product)
            .where(Product.id == product_id)
            .options(
                # load course → instructors → instructor details
                selectinload(Product.course_detail)
                .selectinload(CourseDetail.instructors)
                .selectinload(CourseInstructor.instructor),

                # load skills (via ProductSkill → Skill)
                selectinload(Product.product_skills).selectinload(ProductSkill.skill),

                # load objectives (via ProductObjective → Objective)
                selectinload(Product.product_objectives).selectinload(ProductObjective.objective),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_all_course_product(
            self,
            page: int = 1,
            limit: int = 10,
            category_id: UUID | None = None,
    ) -> list[dict[str, Any]]:
        stmt = (
            select(
                CourseDetail,
                Product.average_rating.label("average_rating")  # 👈 select hybrid_property
            )
            .join(CourseDetail.product)
            .options(
                selectinload(CourseDetail.product)
                .selectinload(Product.product_skills)
                .selectinload(ProductSkill.skill),

                selectinload(CourseDetail.product)
                .selectinload(Product.product_objectives)
                .selectinload(ProductObjective.objective),

                selectinload(CourseDetail.chapters)
                .selectinload(Chapter.videos),
            )
            .order_by(Product.average_rating.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        )

        if category_id:
            stmt = stmt.where(CourseDetail.product.has(Product.category_id == category_id))

        result = await self.db.execute(stmt)
        rows = result.all()

        return [
            {
                "course": row.CourseDetail,
                "average_rating": row.average_rating
            }
            for row in rows
        ]


class ChapterRepository(BaseRepository[Chapter]):
    def __init__(self, db: AsyncSession):
        super().__init__(Chapter, db)

    async def get_chapters_by_course_id(self, course_id: UUID) -> Sequence[Chapter]:
        stmt = (
            select(Chapter)
            .where(Chapter.course_id == course_id)
            .order_by(Chapter.view_index.asc())
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()


class VideoRepository(BaseRepository[Video]):
    def __init__(self, db: AsyncSession):
        super().__init__(Video, db)

    async def get_videos_by_chapter_id(self, chapter_id: UUID) -> Sequence[Video]:
        stmt = (
            select(Video)
            .where(Video.chapter_id == chapter_id)
            .order_by(Video.view_index.asc())
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
