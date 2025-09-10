from typing import Any, Coroutine, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, Row, RowMapping
from uuid import UUID

from app.models.rating import ProductRating
from app.repositories.base_repo import BaseRepository
from app.exceptions.repo_exception import RepoException


class ProductRatingRepository(BaseRepository[ProductRating]):
    def __init__(self, db: AsyncSession):
        super().__init__(ProductRating, db)

    async def get_product_rating(self, product_id: UUID) -> float | None:
        try:
            stmt = (
                select(func.avg(ProductRating.rating))
                .where(ProductRating.product_id == product_id)
            )
            result = await self.db.execute(stmt)
            avg_rating = result.scalar()
            return float(avg_rating) if avg_rating is not None else None
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving product rating",
                additional_info={"error": str(e), "product_id": str(product_id)}
            )

    async def get_product_rate_and_review(self, product_id: UUID) -> Sequence[ProductRating]:
        try:
            stmt = (
                select(ProductRating)
                .where(ProductRating.product_id == product_id)
            )
            result = await self.db.execute(stmt)
            ratings = result.scalars().all()
            return ratings
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving product ratings and reviews",
                additional_info={"error": str(e), "product_id": str(product_id)}
            )
