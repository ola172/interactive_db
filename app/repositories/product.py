from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.repo_exception import RepoException
from app.models import ProductCategory
from app.models.product import Product, ProductType, Level
from app.repositories.base_repo import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: AsyncSession):
        super().__init__(Product, db)

    async def get_all_products_by_type(self, product_type_id: UUID) -> Sequence[Product]:
        try:
            stmt = select(Product).filter(Product.type_id == product_type_id)
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving products by type",
                additional_info={"error": str(e), "product_type_id": str(product_type_id)}
            )

    async def get_all_products_by_category(self, category_id: UUID) -> Sequence[Product]:
        try:
            stmt = select(Product).filter(Product.category_id == category_id)
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving products by category",
                additional_info={"error": str(e), "category_id": str(category_id)}
            )


class ProductTypeRepository(BaseRepository[ProductType]):
    def __init__(self, db: AsyncSession):
        super().__init__(ProductType, db)


class ProductCategoryRepository(BaseRepository[ProductCategory]):
    def __init__(self, db: AsyncSession):
        super().__init__(ProductCategory, db)


class ProductLevelRepository(BaseRepository[Level]):
    def __init__(self, db: AsyncSession):
        super().__init__(Level, db)
