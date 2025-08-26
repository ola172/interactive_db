from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product, ProductType
from app.repositories.base_repo import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: AsyncSession):
        super().__init__(Product, db)

    async def get_all_products_by_type(self, product_type_id: UUID) -> Sequence[Product]:
        stmt = select(Product).filter(Product.type_id == product_type_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()


class ProductTypeRepository(BaseRepository[ProductType]):
    def __init__(self, db: AsyncSession):
        super().__init__(ProductType, db)
