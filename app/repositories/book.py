from typing import Sequence, Optional, Any, Coroutine
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
    ) -> list[dict[str, Any]]:
        """
        Fetch all BookVideoDetail records with related Product, Videos, skills, objectives, and average rating.
        Optionally filter by product category_id.
        """
        stmt = (
            select(BookVideoDetail, Product.average_rating.label("average_rating"))
            .join(BookVideoDetail.product)
            .options(
                selectinload(BookVideoDetail.product).selectinload(Product.skills),
                selectinload(BookVideoDetail.product).selectinload(Product.objectives),
                selectinload(BookVideoDetail.videos),
            )
        )

        if category_id:
            stmt = stmt.where(BookVideoDetail.product.has(Product.category_id == category_id))

        stmt = stmt.offset((page - 1) * limit).limit(limit)
        result = await self.db.execute(stmt)
        rows = result.all()

        return [
            {
                "book_video": row.BookVideoDetail,
                "average_rating": row.average_rating
            }
            for row in rows
        ]

    async def get_by_product_id_with_details(
            self, product_id: UUID
    ) -> Optional[dict[str, Any]]:
        """
        Fetch a single BookVideoDetail by product_id with related Product, Videos, skills, objectives, and average rating.
        """
        stmt = (
            select(BookVideoDetail, Product.average_rating.label("average_rating"))
            .join(BookVideoDetail.product)
            .where(BookVideoDetail.product_id == product_id)
            .options(
                selectinload(BookVideoDetail.product).selectinload(Product.skills),
                selectinload(BookVideoDetail.product).selectinload(Product.objectives),
                selectinload(BookVideoDetail.videos),
            )
        )

        result = await self.db.execute(stmt)
        row = result.one_or_none()

        if not row:
            return None

        return {
            "book_video": row.BookVideoDetail,
            "average_rating": row.average_rating
        }


class BookVideosRepository(BaseRepository[BookVideos]):
    def __init__(self, db: AsyncSession):
        super().__init__(BookVideos, db)


class BookReadingRepository(BaseRepository[BookReadingDetail]):
    def __init__(self, db: AsyncSession):
        super().__init__(BookReadingDetail, db)

    async def get_book_with_sections(self, product_id: UUID) -> dict[str, Any] | None:
        """
        Fetch a single BookReadingDetail by product_id with its sections,
        product details, skills, objectives, and average rating.
        """
        stmt = (
            select(
                BookReadingDetail,
                Product.average_rating.label("average_rating")
            )
            .join(BookReadingDetail.product)  # join with Product
            .options(
                selectinload(BookReadingDetail.product).selectinload(Product.skills),
                selectinload(BookReadingDetail.product).selectinload(Product.objectives),
                selectinload(BookReadingDetail.sections),
            )
            .where(BookReadingDetail.product_id == product_id)
        )

        result = await self.db.execute(stmt)
        row = result.one_or_none()

        if not row:
            return None

        book = row.BookReadingDetail
        average_rating = row.average_rating

        # Ensure sections are ordered
        book.sections.sort(key=lambda s: s.stage_index)

        return {
            "book_reading": book,
            "average_rating": average_rating
        }

    async def get_all_with_details(
            self, page: int = 1, limit: int = 10, category_id: Optional[UUID] = None
    ) -> list[dict[str, Any]]:
        """
        Fetch all BookReadingDetail records with related Product, Sections, skills, and objectives.
        Optionally filter by product category_id.
        """
        stmt = (
            select(
                BookReadingDetail,
                Product.average_rating.label("average_rating")
            )
            .join(BookReadingDetail.product)
            .options(
                selectinload(BookReadingDetail.product).selectinload(Product.skills),
                selectinload(BookReadingDetail.product).selectinload(Product.objectives),
                selectinload(BookReadingDetail.sections),
            )
        )

        if category_id:
            stmt = stmt.where(BookReadingDetail.product.has(Product.category_id == category_id))

        stmt = stmt.offset((page - 1) * limit).limit(limit)
        result = await self.db.execute(stmt)
        rows = result.all()

        return [
            {
                "book_reading": row.BookReadingDetail,
                "average_rating": row.average_rating
            }
            for row in rows
        ]


class BookSectionRepository(BaseRepository[BookSection]):
    def __init__(self, db: AsyncSession):
        super().__init__(BookSection, db)
