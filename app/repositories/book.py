from typing import Optional, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.exceptions.repo_exception import RepoException
from app.models import Product
from app.models.book import BookVideoDetail, BookReadingDetail, BookSection, BookVideos
from app.repositories.base_repo import BaseRepository


class BookVideoDetailsRepository(BaseRepository[BookVideoDetail]):
    def __init__(self, db: AsyncSession):
        super().__init__(BookVideoDetail, db)

    async def get_all_with_details(
            self, page: int = 1, limit: int = 10, category_id: Optional[UUID] = None
    ) -> list[dict[str, Any]]:
        try:
            stmt = (
                select(
                    Product,
                    Product.average_rating.label("average_rating"),
                    Product.book_video_count.label("book_video_count"),
                )
                .options(
                    selectinload(Product.book_video_detail).selectinload(BookVideoDetail.videos),
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
                    "book_video_count": row.book_video_count,
                }
                for row in rows
            ]
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving book videos with details",
                additional_info={"error": str(e), "page": page, "limit": limit,
                                 "category_id": str(category_id) if category_id else None}
            )

    async def get_by_product_id_with_details(self, product_id: UUID) -> Optional[dict[str, Any]]:
        try:
            stmt = (
                select(
                    Product,
                    Product.average_rating.label("average_rating"),
                )
                .where(Product.id == product_id)
                .options(
                    selectinload(Product.book_video_detail).selectinload(BookVideoDetail.videos),
                    selectinload(Product.skills),
                    selectinload(Product.objectives),
                    selectinload(Product.level_obj),
                )
            )

            result = await self.db.execute(stmt)
            row = result.one_or_none()

            if not row:
                return None

            return {
                "product": row.Product,
                "average_rating": row.average_rating,
            }
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving product with book video details",
                additional_info={"error": str(e), "product_id": str(product_id)}
            )


class BookVideosRepository(BaseRepository[BookVideos]):
    def __init__(self, db: AsyncSession):
        super().__init__(BookVideos, db)


class BookReadingRepository(BaseRepository[BookReadingDetail]):
    def __init__(self, db: AsyncSession):
        super().__init__(BookReadingDetail, db)

    async def get_book_with_sections(self, product_id: UUID) -> dict[str, Any] | None:
        try:
            stmt = (
                select(
                    Product,
                    Product.average_rating.label("average_rating"),
                    Product.book_section_count.label("book_section_count"),
                    Product.skill_count.label("skill_count"),
                    Product.objective_count.label("objective_count"),
                )
                .options(
                    selectinload(Product.book_reading_detail).selectinload(BookReadingDetail.sections),
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

            if product.book_reading_detail and product.book_reading_detail.sections:
                product.book_reading_detail.sections.sort(key=lambda s: s.stage_index)

            return {
                "product": product,
                "average_rating": average_rating,
                "book_section_count": book_section_count,
                "skill_count": row.skill_count,
                "objective_count": row.objective_count,

            }
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving book with sections",
                additional_info={"error": str(e), "product_id": str(product_id)}
            )

    async def get_all_with_details(
            self, page: int = 1, limit: int = 10, category_id: Optional[UUID] = None
    ) -> list[dict[str, Any]]:
        try:
            stmt = (
                select(
                    Product,
                    Product.average_rating.label("average_rating"),
                    Product.book_section_count.label("book_section_count"),
                    Product.skill_count.label("skill_count"),
                    Product.objective_count.label("objective_count"),
                )
                .options(
                    selectinload(Product.book_reading_detail).selectinload(BookReadingDetail.sections),
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
                    "skill_count": row.skill_count,
                    "objective_count": row.objective_count,
                }
                for row in rows
            ]
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving all books with details",
                additional_info={"error": str(e), "page": page, "limit": limit,
                                 "category_id": str(category_id) if category_id else None}
            )


class BookSectionRepository(BaseRepository[BookSection]):
    def __init__(self, db: AsyncSession):
        super().__init__(BookSection, db)
