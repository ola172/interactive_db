# app/repositories/skill_objective_repo.py
from typing import Sequence
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.exceptions.repo_exception import RepoException
from app.models.skill_objective import (
    Skill,
    ProductSkill,
    Objective,
    ProductObjective,
)
from app.repositories.base_repo import BaseRepository


class SkillRepository(BaseRepository[Skill]):
    def __init__(self, db: AsyncSession):
        super().__init__(Skill, db)

    async def get_skills_by_product(self, product_id: uuid.UUID) -> Sequence[Skill]:
        """Get all skills linked to a specific product"""
        try:
            stmt = (
                select(Skill)
                .join(ProductSkill, ProductSkill.skill_id == Skill.id)
                .where(ProductSkill.product_id == product_id)
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving skills by product",
                additional_info={"error": str(e), "product_id": product_id},
            )


class ProductSkillRepository(BaseRepository[ProductSkill]):
    def __init__(self, db: AsyncSession):
        super().__init__(ProductSkill, db)

    async def get_skills_by_product_id(self, product_id: uuid.UUID) -> Sequence[ProductSkill]:
        """Get all ProductSkill relations for a specific product"""
        try:
            stmt = select(ProductSkill).where(ProductSkill.product_id == product_id)
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving product skills",
                additional_info={"error": str(e), "product_id": product_id},
            )


class ObjectiveRepository(BaseRepository[Objective]):
    def __init__(self, db: AsyncSession):
        super().__init__(Objective, db)

    async def get_objectives_by_product(self, product_id: uuid.UUID) -> Sequence[Objective]:
        """Get all objectives linked to a specific product"""
        try:
            stmt = (
                select(Objective)
                .join(ProductObjective, ProductObjective.objective_id == Objective.id)
                .where(ProductObjective.product_id == product_id)
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving objectives by product",
                additional_info={"error": str(e), "product_id": product_id},
            )


class ProductObjectiveRepository(BaseRepository[ProductObjective]):
    def __init__(self, db: AsyncSession):
        super().__init__(ProductObjective, db)

    async def get_objectives_by_product_id(self, product_id: uuid.UUID) -> Sequence[ProductObjective]:
        """Get all ProductObjective relations for a specific product"""
        try:
            stmt = select(ProductObjective).where(ProductObjective.product_id == product_id)
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise RepoException(
                status_code=500,
                detail="Error retrieving product objectives",
                additional_info={"error": str(e), "product_id": product_id},
            )
