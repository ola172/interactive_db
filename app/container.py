from typing import Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Database
from app.repositories import (ProductTypeRepository, ProductRepository,
                              CourseDetailRepository, ChapterRepository, VideoRepository, InstructorRepository,
                              CourseCategoryRepository)
from app.services import CourseService
from app.services import ProductService
from app.services.instructor_service import InstructorService

db = Database()


async def get_db_session() -> AsyncGenerator[AsyncSession, Any]:
    async for session in db.get_session():
        yield session


async def get_product_type_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[ProductTypeRepository, Any]:
    yield ProductTypeRepository(session)


async def get_product_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[ProductRepository, Any]:
    yield ProductRepository(session)


async def get_instructor_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[InstructorRepository, Any]:
    yield InstructorRepository(session)


async def get_course_detail_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[CourseDetailRepository, Any]:
    yield CourseDetailRepository(session)

async def get_course_category_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[CourseCategoryRepository, Any]:
    yield CourseCategoryRepository(session)


async def get_chapter_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[ChapterRepository, Any]:
    yield ChapterRepository(session)


async def get_video_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[VideoRepository, Any]:
    yield VideoRepository(session)


async def get_course_service(
        course_detail_repo: CourseDetailRepository = Depends(get_course_detail_repository),
        course_category_repo: CourseCategoryRepository = Depends(get_course_category_repository),
        chapter_repo: ChapterRepository = Depends(get_chapter_repository),
        video_repo: VideoRepository = Depends(get_video_repository),
        product_repo: ProductRepository = Depends(get_product_repository),
) -> AsyncGenerator["CourseService", Any]:
    yield CourseService(course_detail_repo=course_detail_repo,
                        course_category_repo=course_category_repo,
                        chapter_repo=chapter_repo,
                        video_repo=video_repo,
                        product_repo=product_repo,
                        db=course_detail_repo.db)


async def get_instructor_service(
        instructor_repo: InstructorRepository = Depends(get_instructor_repository),
) -> AsyncGenerator["InstructorService", Any]:
    yield InstructorService(
        instructor_repository=instructor_repo,
    )


async def get_product_service(
        product_repository: ProductRepository = Depends(get_product_repository),
        product_type_repository: ProductTypeRepository = Depends(get_product_type_repository),
        course_service: CourseService = Depends(get_course_service),
) -> AsyncGenerator["ProductService", Any]:
    yield ProductService(
        product_repository=product_repository,
        product_type_repository=product_type_repository,
        course_service=course_service,
        db=product_repository.db,
    )
