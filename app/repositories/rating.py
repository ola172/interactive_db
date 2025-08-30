from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rating import ProductRating
from app.repositories.base_repo import BaseRepository
from sqlalchemy import select, func
from uuid import UUID

class ProductRatingRepository(BaseRepository[ProductRating]):
    def __init__(self, db: AsyncSession):
        super().__init__(ProductRating, db)

    async def get_product_rating(self, product_id: UUID) -> float | None:
        stmt = (
            select(func.avg(ProductRating.rating))
            .where(ProductRating.product_id == product_id)
        )
        result = await self.db.execute(stmt)
        avg_rating = result.scalar()
        return float(avg_rating) if avg_rating is not None else None
