import uuid
from typing import Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.exceptions.repo_exception import RepoException
from app.models import Product
from app.models.pathway import Pathway, PathwayItem
from app.repositories.base_repo import BaseRepository


class PathwayRepository(BaseRepository[Pathway]):
    def __init__(self, db: AsyncSession):
        super().__init__(Pathway, db)

    async def get_pathway_by_id(self, pathway_id: uuid.UUID) -> Optional[dict[str, Any]]:
        """
        Fetch a single Pathway by ID with its items, products, and average ratings.
        """
        try:
            stmt = (
                select(Pathway, Product.average_rating.label("average_rating"))
                .where(Pathway.id == pathway_id)
                .join(Pathway.product)  # Join the main product for average_rating
                .options(
                    selectinload(Pathway.items).selectinload(PathwayItem.product),
                    selectinload(Pathway.items).selectinload(PathwayItem.product),
                    selectinload(Pathway.product).selectinload(Product.skills),
                    selectinload(Pathway.product).selectinload(Product.objectives),
                )
            )

            result = await self.db.execute(stmt)
            row = result.one_or_none()

            if not row:
                return None

            return {
                "pathway": row.Pathway,
                "average_rating": row.average_rating
            }
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving pathway by id",
                additional_info={"error": str(e), "pathway_id": str(pathway_id)}
            )

    async def get_all_pathways(
            self, page: int = 1, limit: int = 10, category_id: Optional[uuid.UUID] = None
    ) -> list[dict[str, Any]]:
        """
        Fetch all Pathways with their items, products, and average ratings.
        Optionally filter by product category_id.
        """
        try:
            stmt = (
                select(Pathway, Product.average_rating.label("average_rating"))
                .join(Pathway.product)
                .options(
                    selectinload(Pathway.items).selectinload(PathwayItem.product).selectinload(Product.skills),
                    selectinload(Pathway.items).selectinload(PathwayItem.product).selectinload(Product.objectives),
                    selectinload(Pathway.product).selectinload(Product.skills),
                    selectinload(Pathway.product).selectinload(Product.objectives),
                )
            )

            if category_id:
                stmt = stmt.where(Product.category_id == category_id)

            stmt = stmt.offset((page - 1) * limit).limit(limit)

            result = await self.db.execute(stmt)
            rows = result.all()

            return [
                {
                    "pathway": row.Pathway,
                    "average_rating": row.average_rating
                }
                for row in rows
            ]
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving all pathways",
                additional_info={
                    "error": str(e),
                    "page": page,
                    "limit": limit,
                    "category_id": str(category_id) if category_id else None,
                }
            )


class PathwayItemRepository(BaseRepository[PathwayItem]):
    def __init__(self, db: AsyncSession):
        super().__init__(PathwayItem, db)
