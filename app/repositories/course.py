from typing import Sequence, Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Product, ProductSkill
from app.models.course import CourseDetail, Chapter, Video, CourseInstructor
from app.models.product import Level
from app.models.skill_objective import ProductObjective
from app.repositories.base_repo import BaseRepository


class CourseDetailRepository(BaseRepository[CourseDetail]):
    def __init__(self, db: AsyncSession, ):
        super().__init__(CourseDetail, db)

    async def get_course_product(self, product_id: UUID) -> dict[str, Any] | None:
        stmt = (
            select(
                Product,
                Product.average_rating.label("average_rating"),
                Product.chapter_count.label("chapter_count"),
                Product.video_count.label("video_count"),
            )
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

                # load level relationship from levels table
                selectinload(Product.level_obj),

                # load chapters and videos via course_detail
                selectinload(Product.course_detail)
                .selectinload(CourseDetail.chapters)
                .selectinload(Chapter.videos),
            )
        )

        result = await self.db.execute(stmt)
        row = result.first()

        if not row:
            return None

        product = row.Product

        return {
            "product": product,
            "average_rating": row.average_rating,
            "chapter_count": row.chapter_count,
            "video_count": row.video_count,
        }


    async def get_all_course_product(
        self,
        page: int = 1,
        limit: int = 10,
        category_id: UUID | None = None,
    ) -> list[dict[str, Any]]:
        stmt = (
            select(
                Product,
                Product.average_rating.label("average_rating"),
                Product.chapter_count.label("chapter_count"),
                Product.video_count.label("video_count"),
            )
            .options(
                # course → instructors → instructor details
                selectinload(Product.course_detail)
                .selectinload(CourseDetail.instructors)
                .selectinload(CourseInstructor.instructor),

                # skills
                selectinload(Product.product_skills).selectinload(ProductSkill.skill),

                # objectives
                selectinload(Product.product_objectives).selectinload(ProductObjective.objective),

                # level
                selectinload(Product.level_obj),

                # chapters → videos
                selectinload(Product.course_detail)
                .selectinload(CourseDetail.chapters)
                .selectinload(Chapter.videos),
            )
            .order_by(Product.average_rating.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        )

        if category_id:
            stmt = stmt.where(Product.category_id == category_id)

        result = await self.db.execute(stmt)
        rows = result.all()

        return [
            {
                "product": row.Product,
                "average_rating": row.average_rating,
                "chapter_count": row.chapter_count,
                "video_count": row.video_count,
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
