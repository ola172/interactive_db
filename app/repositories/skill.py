# app/repositories/skill_objective_repo.py
from typing import Any, Coroutine, Sequence

from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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

    async def get_skills_by_product(self, product_id: str) -> Sequence[Skill]:
        """Get all skills linked to a specific product"""
        stmt = (
            select(Skill)
            .join(ProductSkill, ProductSkill.skill_id == Skill.id)
            .where(ProductSkill.product_id == product_id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()


class ProductSkillRepository(BaseRepository[ProductSkill]):
    def __init__(self, db: AsyncSession):
        super().__init__(ProductSkill, db)


class ObjectiveRepository(BaseRepository[Objective]):
    def __init__(self, db: AsyncSession):
        super().__init__(Objective, db)

    async def get_objectives_by_product(self, product_id: str) -> Sequence[Objective]:
        """Get all objectives linked to a specific product"""
        stmt = (
            select(Objective)
            .join(ProductObjective, ProductObjective.objective_id == Objective.id)
            .where(ProductObjective.product_id == product_id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

class ProductObjectiveRepository(BaseRepository[ProductObjective]):
    def __init__(self, db: AsyncSession):
        super().__init__(ProductObjective, db)
