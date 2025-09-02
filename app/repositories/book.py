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
        Fetch all Products with related BookVideoDetail (including BookVideos),
        skills, objectives, level, average rating, and book video count.
        Optionally filter by product category_id.
        """
        stmt = (
            select(
                Product,
                Product.average_rating.label("average_rating"),
                Product.book_video_count.label("book_video_count"),  # ✅ add book video count
            )
            .options(
                # load BookVideoDetail and its BookVideos
                selectinload(Product.book_video_detail)
                .selectinload(BookVideoDetail.videos),

                # load skills
                selectinload(Product.skills),

                # load objectives
                selectinload(Product.objectives),

                # load level relationship
                selectinload(Product.level_obj),
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
                "book_video_count": row.book_video_count,
            }
            for row in rows
        ]

    async def get_by_product_id_with_details(
            self, product_id: UUID
    ) -> Optional[dict[str, Any]]:
        """
        Fetch a single Product by product_id with related BookVideoDetail (including Videos),
        skills, objectives, level, and average rating.
        """
        stmt = (
            select(
                Product,
                Product.average_rating.label("average_rating"),
            )
            .where(Product.id == product_id)
            .options(
                # load BookVideoDetail and its Videos
                selectinload(Product.book_video_detail)
                .selectinload(BookVideoDetail.videos),

                # load skills
                selectinload(Product.skills),

                # load objectives
                selectinload(Product.objectives),

                # load level relationship
                selectinload(Product.level_obj),
            )
        )

        result = await self.db.execute(stmt)
        row = result.one_or_none()

        if not row:
            return None

        return {
            "product": row.Product,  # includes book_video_detail + videos
            "average_rating": row.average_rating,
        }


class BookVideosRepository(BaseRepository[BookVideos]):
    def __init__(self, db: AsyncSession):
        super().__init__(BookVideos, db)


class BookReadingRepository(BaseRepository[BookReadingDetail]):
    def __init__(self, db: AsyncSession):
        super().__init__(BookReadingDetail, db)

    async def get_book_with_sections(self, product_id: UUID) -> dict[str, Any] | None:
        """
        Fetch a single Product by product_id with its BookReadingDetail, Sections,
        skills, objectives, average rating, and section count.
        """
        stmt = (
            select(
                Product,
                Product.average_rating.label("average_rating"),
                Product.book_section_count.label("book_section_count"),  # ✅ from Product hybrid
            )
            .options(
                selectinload(Product.book_reading_detail)
                .selectinload(BookReadingDetail.sections),

                selectinload(Product.skills),
                selectinload(Product.objectives),
                selectinload(Product.level_obj),
            )
            .where(Product.id == product_id)
        )

        result = await self.db.execute(stmt)
        row = result.one_or_none()

        if not row:
            return None

        product = row.Product
        average_rating = row.average_rating
        book_section_count = row.book_section_count

        # Ensure sections are ordered if book exists
        if product.book_reading_detail and product.book_reading_detail.sections:
            product.book_reading_detail.sections.sort(key=lambda s: s.stage_index)

        return {
            "product": product,
            "average_rating": average_rating,
            "book_section_count": book_section_count,
        }

    async def get_all_with_details(
            self, page: int = 1, limit: int = 10, category_id: Optional[UUID] = None
    ) -> list[dict[str, Any]]:
        """
        Fetch all Products with related BookReadingDetail (including Sections),
        skills, objectives, level, average rating, and section count.
        Optionally filter by product category_id.
        """
        stmt = (
            select(
                Product,
                Product.average_rating.label("average_rating"),
                Product.book_section_count.label("book_section_count"),  # ✅ from Product hybrid
            )
            .options(
                selectinload(Product.book_reading_detail)
                .selectinload(BookReadingDetail.sections),

                selectinload(Product.skills),
                selectinload(Product.objectives),
                selectinload(Product.level_obj),
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
                "book_section_count": row.book_section_count,
            }
            for row in rows
        ]


class BookSectionRepository(BaseRepository[BookSection]):
    def __init__(self, db: AsyncSession):
        super().__init__(BookSection, db)
