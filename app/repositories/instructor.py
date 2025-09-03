import uuid
from typing import Any, Coroutine, Sequence

from sqlalchemy import select, func, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Instructor, InstructorSkill, CourseInstructor
from app.models.instructor import InstructorRating
from app.repositories.base_repo import BaseRepository


class InstructorRepository(BaseRepository[Instructor]):
    def __init__(self, db: AsyncSession):
        super().__init__(Instructor, db)


class InstructorSkillRepository(BaseRepository[InstructorSkill]):
    def __init__(self, db: AsyncSession):
        super().__init__(InstructorSkill, db)


class CourseInstructorRepository(BaseRepository[CourseInstructor]):
    def __init__(self, db: AsyncSession):
        super().__init__(CourseInstructor, db)


class InstructorRateRepository(BaseRepository[InstructorRating]):
    def __init__(self, db: AsyncSession):
        super().__init__(InstructorRating, db)

    async def get_instructor_average_rating(self, instructor_id: uuid.UUID) -> float:
        stmt = select(func.avg(InstructorRating.rating)).where(
            InstructorRating.instructor_id == instructor_id
        )
        result = await self.db.execute(stmt)
        avg_rating = result.scalar()
        return round(avg_rating or 0.0, 2)


    async def get_all_ratings_for_instructor(self, instructor_id: uuid.UUID) -> Sequence[InstructorRating]:
        """
        Fetch all ratings for a specific instructor.
        """
        stmt = select(InstructorRating).where(InstructorRating.instructor_id == instructor_id)
        result = await self.db.execute(stmt)
        ratings = result.scalars().all()
        return ratings
