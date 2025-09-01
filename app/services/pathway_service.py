import uuid
from typing import Optional

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import Pathway, PathwayItem
from app.repositories import (PathwayRepository, PathwayItemRepository,
                              ProductRepository,
                              ProductObjectiveRepository, ProductSkillRepository)
from app.schemas.pathway_schema import PathwayCreateWithProduct


class PathwayService:
    def __init__(self, db,
                 product_repo: ProductRepository,
                 skill_repository: ProductSkillRepository,
                 objective_repository: ProductObjectiveRepository,
                 pathway_repo: PathwayRepository, pathway_item_repo: PathwayItemRepository):
        self.db = db
        self.pathway_repo = pathway_repo
        self.pathway_item_repo = pathway_item_repo
        self.product_repo = product_repo
        self.skill_repo = skill_repository
        self.objective_repo = objective_repository

    async def create_pathway_with_product(self, pathway_data: PathwayCreateWithProduct) -> uuid.UUID:
        """
        Create a new product and pathway along with pathway items,
        optionally assigning skills and objectives to the product.
        """
        async with self.db.begin():  # ensure atomic transaction

            # 1️⃣ Create Product
            product_data = pathway_data.product
            product = await self.product_repo.create({
                "type_id": product_data.type_id,
                "category_id": product_data.category_id,
                "title": product_data.title,
                "description": product_data.description,
                "language": product_data.language,
                "level": product_data.level,
                "duration": product_data.duration,
                "price": product_data.price,
                "cover": product_data.cover,
                "short_video": product_data.short_video,
            })

            # 2️⃣ Assign Skills (many-to-many)
            for skill_id in product_data.skills:
                await self.skill_repo.create({
                    "product_id": product.id,
                    "skill_id": skill_id,
                })

            # 3️⃣ Assign Objectives (many-to-many)
            for objective_id in product_data.objectives:
                await self.objective_repo.create({
                    "product_id": product.id,
                    "objective_id": objective_id,
                })

            # 4️⃣ Create Pathway linked to Product
            pathway = await self.pathway_repo.create({
                "name": pathway_data.name,
                "description": pathway_data.description,
                "product_id": product.id,
            })

            # 5️⃣ Create Pathway Items
            for index, item in enumerate(pathway_data.items):
                await self.pathway_item_repo.create({
                    "pathway_id": pathway.id,
                    "product_id": item.product_id,
                    "order_index": item.order_index or (index + 1),
                })

        # ✅ Transaction committed automatically if no errors
        return pathway.id

    async def get_pathway_by_id(self, pathway_id: uuid.UUID):
        return await self.pathway_repo.get_pathway_by_id(pathway_id)

    async def get_all_pathways(self, page: int = 1, limit: int = 10, category_id: Optional[uuid.UUID] = None):
        return await self.pathway_repo.get_all_pathways(page, limit, category_id)
