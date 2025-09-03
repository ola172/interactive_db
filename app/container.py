from typing import Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Database
from app.repositories import (ProductTypeRepository, ProductRepository,
                              CourseDetailRepository, ChapterRepository,
                              VideoRepository, InstructorRepository,
                              CourseInstructorRepository,
                              ProductRatingRepository,
                              SkillRepository, ObjectiveRepository,
                              BookReadingRepository, BookSectionRepository,
                              ProductSkillRepository, ProductObjectiveRepository,
                              BookVideosRepository, PathwayRepository,
                              PathwayItemRepository,
                              ProductLevelRepository,
                              ProductCategoryRepository, BookVideoDetailsRepository)
from app.repositories.instructor import InstructorRateRepository
from app.repositories.user import UserRepository, UserProductRepository, UserWaitingListRepository
from app.services import CourseService
from app.services import ProductService
from app.services.book_reading_service import BookService
from app.services.book_video_service import BookVideoService
from app.services.instructor_service import InstructorService
from app.services.pathway_service import PathwayService
from app.services.user_service import UserService

db = Database()

async def get_db_session() -> AsyncGenerator[AsyncSession, Any]:
    async for session in db.get_session():
        yield session


async def get_user_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[UserRepository, Any]:
    yield UserRepository(session)

async def get_instructor_rate_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[InstructorRateRepository, Any]:
    yield InstructorRateRepository(session)


async def get_user_product_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[UserProductRepository, Any]:
    yield UserProductRepository(session)

async def get_product_level_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[ProductLevelRepository, Any]:
    yield ProductLevelRepository(session)

async def get_user_waiting_list_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[UserWaitingListRepository, Any]:
    yield UserWaitingListRepository(session)


async def get_pathway_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[PathwayRepository, Any]:
    yield PathwayRepository(session)


async def get_pathway_item_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[PathwayItemRepository, Any]:
    yield PathwayItemRepository(session)


async def get_book_reading_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[BookReadingRepository, Any]:
    yield BookReadingRepository(session)


async def get_book_video_details_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[BookVideoDetailsRepository, Any]:
    yield BookVideoDetailsRepository(session)


async def get_book_videos_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[BookVideosRepository, Any]:
    yield BookVideosRepository(session)


async def get_book_section_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[BookSectionRepository, Any]:
    yield BookSectionRepository(session)


async def get_product_rating_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[ProductRatingRepository, Any]:
    yield ProductRatingRepository(session)


async def get_skill_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[SkillRepository, Any]:
    yield SkillRepository(session)


async def get_product_skill_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[ProductSkillRepository, Any]:
    yield ProductSkillRepository(session)


async def get_product_objective_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[ProductObjectiveRepository, Any]:
    yield ProductObjectiveRepository(session)


async def get_objective_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[ObjectiveRepository, Any]:
    yield ObjectiveRepository(session)


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


async def get_course_instructor_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[CourseInstructorRepository, Any]:
    yield CourseInstructorRepository(session)


async def get_course_detail_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[CourseDetailRepository, Any]:
    yield CourseDetailRepository(session)


async def get_product_category_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[ProductCategoryRepository, Any]:
    yield ProductCategoryRepository(session)


async def get_chapter_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[ChapterRepository, Any]:
    yield ChapterRepository(session)


async def get_video_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[VideoRepository, Any]:
    yield VideoRepository(session)


async def get_user_service(
        user_repo: UserRepository = Depends(get_user_repository),
        user_product_repo: UserProductRepository = Depends(get_user_product_repository),
        instructor_rate_repo: InstructorRateRepository = Depends(get_instructor_rate_repository),
        waiting_repo: UserWaitingListRepository = Depends(get_user_waiting_list_repository),
) -> AsyncGenerator["UserService", Any]:
    yield UserService(db=user_repo.db,
                      user_repo=user_repo,
                      user_product_repo=user_product_repo,
                      instructor_rate_repo=instructor_rate_repo,
                      waiting_repo=waiting_repo)


async def get_pathway_service(
        pathway_repo: PathwayRepository = Depends(get_pathway_repository),
        pathway_item_repo: PathwayItemRepository = Depends(get_pathway_item_repository),
        product_repo: ProductRepository = Depends(get_product_repository),
        product_skill_repo: ProductSkillRepository = Depends(get_product_skill_repository),
        product_objective_repo: ProductObjectiveRepository = Depends(get_product_objective_repository),
) -> AsyncGenerator["PathwayService", Any]:
    yield PathwayService(db=pathway_repo.db,
                         pathway_repo=pathway_repo,
                         pathway_item_repo=pathway_item_repo,
                         product_repo=product_repo,
                         skill_repository=product_skill_repo,
                         objective_repository=product_objective_repo, )


async def get_course_service(
        course_detail_repo: CourseDetailRepository = Depends(get_course_detail_repository),
        chapter_repo: ChapterRepository = Depends(get_chapter_repository),
        video_repo: VideoRepository = Depends(get_video_repository),
        product_skill_repo: ProductSkillRepository = Depends(get_product_skill_repository),
        product_objective_repo: ProductObjectiveRepository = Depends(get_product_objective_repository),
        course_instructor_repo: CourseInstructorRepository = Depends(get_course_instructor_repository),
        product_rating_repo: ProductRatingRepository = Depends(get_product_rating_repository),
        product_repo: ProductRepository = Depends(get_product_repository),
) -> AsyncGenerator["CourseService", Any]:
    yield CourseService(course_detail_repo=course_detail_repo,
                        chapter_repo=chapter_repo,
                        video_repo=video_repo,
                        product_skill_repo=product_skill_repo,
                        product_objective_repo=product_objective_repo,
                        course_instructor_repo=course_instructor_repo,
                        product_repo=product_repo,
                        product_rating_repo=product_rating_repo,
                        db=course_detail_repo.db)


async def get_instructor_service(
        instructor_repo: InstructorRepository = Depends(get_instructor_repository),
        instructor_rate_repo: InstructorRateRepository = Depends(get_instructor_rate_repository)
) -> AsyncGenerator["InstructorService", Any]:
    yield InstructorService(
        instructor_repository=instructor_repo,
        instructor_rate_repo=instructor_rate_repo,
    )


async def get_book_service(
        book_reading_repo: BookReadingRepository = Depends(get_book_reading_repository),
        product_repo: ProductRepository = Depends(get_product_repository),
        book_section_repo: BookSectionRepository = Depends(get_book_section_repository),
        product_skill_repo: ProductSkillRepository = Depends(get_product_skill_repository),
        product_objective_repo: ProductObjectiveRepository = Depends(get_product_objective_repository),

) -> AsyncGenerator["BookService", Any]:
    yield BookService(
        book_reading_repo=book_reading_repo,
        product_repo=product_repo,
        book_section_repo=book_section_repo,
        product_skill_repo=product_skill_repo,
        product_objective_repo=product_objective_repo,
        db=book_reading_repo.db,
    )


async def get_product_service(
        product_repository: ProductRepository = Depends(get_product_repository),
        product_type_repository: ProductTypeRepository = Depends(get_product_type_repository),
        product_category_repo: ProductCategoryRepository = Depends(get_product_category_repository),
        skill_repository: SkillRepository = Depends(get_skill_repository),
        objective_repository: ObjectiveRepository = Depends(get_objective_repository),
        product_rating_repo: ProductRatingRepository = Depends(get_product_rating_repository),
        product_level_repository: ProductLevelRepository = Depends(get_product_level_repository),
        course_service: CourseService = Depends(get_course_service),
) -> AsyncGenerator["ProductService", Any]:
    yield ProductService(
        product_repository=product_repository,
        product_type_repository=product_type_repository,
        course_service=course_service,
        product_category_repo=product_category_repo,
        skill_repository=skill_repository,
        objective_repository=objective_repository,
        product_rating_repository=product_rating_repo,
        product_level_repository=product_level_repository,
        db=product_repository.db,
    )


async def get_book_video_service(
        book_video_details_repo: BookVideoDetailsRepository = Depends(get_book_video_details_repository),
        book_videos_repo: BookVideosRepository = Depends(get_book_videos_repository),
        product_repo: ProductRepository = Depends(get_product_repository),
        product_skill_repo: ProductSkillRepository = Depends(get_product_skill_repository),
        product_objective_repo: ProductObjectiveRepository = Depends(get_product_objective_repository),
) -> AsyncGenerator["BookVideoService", Any]:
    yield BookVideoService(
        book_video_details_repo=book_video_details_repo,
        book_videos_repo=book_videos_repo,
        product_repo=product_repo,
        product_skill_repo=product_skill_repo,
        product_objective_repo=product_objective_repo,
        db=book_video_details_repo.db,
    )
