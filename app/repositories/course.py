from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Product
from app.models.course import CourseDetail, Chapter, Video, CourseCategory
from app.repositories.base_repo import BaseRepository


class CourseDetailRepository(BaseRepository[CourseDetail]):
    def __init__(self, db: AsyncSession):
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
                selectinload(Product.course_detail)
                .selectinload(CourseDetail.chapters)
                .selectinload(Chapter.videos)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_all_course_product(
            self, page: int = 1, limit: int = 10
    ) -> Sequence[CourseDetail]:
        stmt = (
            select(CourseDetail)
            .options(
                selectinload(CourseDetail.product),
                selectinload(CourseDetail.chapters)
                .selectinload(Chapter.videos)
            )
            .offset((page - 1) * limit)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()


class ChapterRepository(BaseRepository[Chapter]):
    def __init__(self, db: AsyncSession):
        super().__init__(Chapter, db)

    async def get_chapters_by_course_id(self, course_id: UUID) -> Sequence[Chapter]:
        stmt = (
            select(Chapter)
            .where(Chapter.course_id == course_id)
            .order_by(Chapter.order_index.asc())
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
            .order_by(Video.order_index.asc())
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

class CourseCategoryRepository(BaseRepository[CourseCategory]):
    def __init__(self, db: AsyncSession):
        super().__init__(CourseCategory, db)
