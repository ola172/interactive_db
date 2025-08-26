import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import InstructorRepository
from app.schemas.instructor import InstructorBase

class InstructorService:
    def __init__(self, instructor_repository: InstructorRepository):
        self.instructor_repository = instructor_repository
        self.db: AsyncSession = instructor_repository.db

    async def get_all_instructors(self, page: int = 1, limit: int = 10):
        return await self.instructor_repository.get_all(page, limit)

    async def create_instructor(self, instructor_request: InstructorBase):
        async with self.db.begin():  # Transaction block
            instructor = await self.instructor_repository.create(instructor_request.model_dump())
        return instructor

    async def get_instructor_by_id(self, instructor_id: uuid.UUID):
        return await self.instructor_repository.get(instructor_id)
