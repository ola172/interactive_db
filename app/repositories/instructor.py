from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Instructor, InstructorSkill, CourseInstructor
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
