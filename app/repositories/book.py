from typing import Sequence, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Product
from app.models.book import BookVideoDetail, BookReadingDetail, BookSection, BookVideos
from app.repositories.base_repo import BaseRepository


class BookVideoDetailsRepository(BaseRepository[BookVideoDetail]):
    def __init__(self, db: AsyncSession):
        super().__init__(BookVideoDetail, db)

    async def get_all_with_details(
            self, page: int = 1, limit: int = 10, category_id: Optional[UUID] = None
    ) -> Sequence[BookVideoDetail]:
        """
        Fetch all BookVideoDetail records with related Product, Videos, skills, and objectives.
        Optionally filter by product category_id.
        """
        stmt = (
            select(BookVideoDetail)
            .options(
                selectinload(BookVideoDetail.product).selectinload(Product.skills),
                selectinload(BookVideoDetail.product).selectinload(Product.objectives),
                selectinload(BookVideoDetail.videos),
            )
        )

        # ✅ Add dynamic filter if category_id is provided
        if category_id:
            stmt = stmt.where(BookVideoDetail.product.has(Product.category_id == category_id))

        stmt = stmt.offset((page - 1) * limit).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_product_id_with_details(self, product_id: UUID) -> Optional[BookVideoDetail]:
        """
        Fetch a single BookVideoDetail by product_id with related Product, Videos, skills, and objectives.
        """
        stmt = (
            select(BookVideoDetail)
            .join(Product)
            .where(Product.id == product_id)
            .options(
                selectinload(BookVideoDetail.product)
                .selectinload(Product.skills),
                selectinload(BookVideoDetail.product)
                .selectinload(Product.objectives),
                selectinload(BookVideoDetail.videos),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()


class BookVideosRepository(BaseRepository[BookVideos]):
    def __init__(self, db: AsyncSession):
        super().__init__(BookVideos, db)


class BookReadingRepository(BaseRepository[BookReadingDetail]):
    def __init__(self, db: AsyncSession):
        super().__init__(BookReadingDetail, db)

    async def get_book_with_sections(self, book_id: UUID) -> BookReadingDetail:
        stmt = (
            select(BookReadingDetail)
            .where(BookReadingDetail.id == book_id)
            .options(
                selectinload(BookReadingDetail.sections)
            )
        )

        result = await self.db.execute(stmt)
        book = result.scalar_one_or_none()

        if book:
            # Ensure sections are ordered
            book.sections.sort(key=lambda s: s.stage_index)

        return book

    async def get_all_with_details(
            self, page: int = 1, limit: int = 10, category_id: Optional[UUID] = None
    ) -> Sequence[BookReadingDetail]:
        """
        Fetch all BookReadingDetail records with related Product, Sections, skills, and objectives.
        Optionally filter by product category_id.
        """
        stmt = (
            select(BookReadingDetail)
            .options(
                selectinload(BookReadingDetail.product).selectinload(Product.skills),
                selectinload(BookReadingDetail.product).selectinload(Product.objectives),
                selectinload(BookReadingDetail.sections),
            )
        )

        # ✅ Add dynamic filter if category_id is provided
        if category_id:
            stmt = stmt.where(BookReadingDetail.product.has(Product.category_id == category_id))

        stmt = stmt.offset((page - 1) * limit).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().unique().all()


class BookSectionRepository(BaseRepository[BookSection]):
    def __init__(self, db: AsyncSession):
        super().__init__(BookSection, db)
