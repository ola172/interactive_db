import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Pathway, PathwayItem
from app.repositories import PathwayRepository, PathwayItemRepository
from app.schemas.pathway_schema import PathwayCreate


class PathwayService:
    def __init__(self, db, pathway_repo: PathwayRepository, pathway_item_repo: PathwayItemRepository):
        self.db = db
        self.pathway_repo = pathway_repo
        self.pathway_item_repo = pathway_item_repo

    async def create_pathway(self, pathway_data: PathwayCreate) -> uuid.UUID:
        async with self.db.begin():
            # 1. Create Pathway
            pathway = await self.pathway_repo.create({
                "name": pathway_data.name,
                "description": pathway_data.description,
            })

            # 2. Create Items
            for index, item in enumerate(pathway_data.items):
                await self.pathway_item_repo.create({
                    "pathway_id": pathway.id,
                    "product_id": item.product_id,
                    "order_index": item.order_index or (index + 1),
                })

        return pathway.id

    async def get_pathway_by_id(self, pathway_id: uuid.UUID):
        stmt = (
            select(Pathway)
            .where(Pathway.id == pathway_id)
            .options(
                selectinload(Pathway.items).selectinload(PathwayItem.product),
                selectinload(Pathway.product)  # main product of pathway if needed
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_pathways(self):
        stmt = select(Pathway).options(
            selectinload(Pathway.items).selectinload(PathwayItem.product),
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
