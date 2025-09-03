import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import InstructorRepository
from app.repositories.instructor import InstructorRateRepository
from app.schemas.instructor import InstructorBase
from app.exceptions.custom_exception import CustomException
from app.exceptions.service_exception import ServiceException


class InstructorService:
    def __init__(self, instructor_repository: InstructorRepository,
                 instructor_rate_repo: InstructorRateRepository):
        self.instructor_repository = instructor_repository
        self.db: AsyncSession = instructor_repository.db
        self.instructor_rate_repo = instructor_rate_repo

    async def get_all_instructors(self, page: int = 1, limit: int = 10):
        try:
            return await self.instructor_repository.get_all(page, limit)
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch instructors",
                additional_info={"error": str(e), "page": page, "limit": limit},
            )

    async def create_instructor(self, instructor_request: InstructorBase):
        try:
            async with self.db.begin():  # Transaction block
                instructor = await self.instructor_repository.create(
                    instructor_request.model_dump()
                )
            return instructor
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create instructor",
                additional_info={"error": str(e), "data": instructor_request.model_dump()},
            )

    async def get_instructor_by_id(self, instructor_id: uuid.UUID):
        try:
            return await self.instructor_repository.get(instructor_id)
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch instructor by id",
                additional_info={"error": str(e), "instructor_id": str(instructor_id)},
            )

    async def get_instructor_average_rating(self, instructor_id: uuid.UUID):
        try:
            return await self.instructor_rate_repo.get_instructor_average_rating(instructor_id)
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch instructor average rating",
                additional_info={"error": str(e), "instructor_id": str(instructor_id)},
            )

    async def get_instructor_rating(self, instructor_id: uuid.UUID):
        try:
            return await self.instructor_rate_repo.get_all_ratings_for_instructor(instructor_id=instructor_id)
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch instructor average rating",
                additional_info={"error": str(e), "instructor_id": str(instructor_id)},
            )