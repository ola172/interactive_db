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
from app.repositories.interactive_repositories import (
    InteractiveCourseDetailsRepository,
    InteractiveChapterRepository,
    InteractiveVideoRepository,
    InteractiveParagraphRepository,
    InteractiveWordRepository,
    InteractiveKeyWordRepository,
    KeyWordTypeRepository,
    VideoKeywordTypeStyleRepository,
    VisualItemRepository,
    VisualTypeRepository,
    TableDataRepository,
    ChartDataRepository,
    ImageRepository,
    WordTypeRepository,
)
from app.repositories.interactive_repositories.assist_file_repository import AssistFileRepository, FileTypeRepository
from app.repositories.interactive_repositories.assist_image_repository import AssistImageRepository
from app.repositories.instructor import InstructorRateRepository
from app.repositories.interactive_repositories.interactive_visual_repository import ChartTypeRepository
from app.repositories.user import UserRepository, UserProductRepository, UserWaitingListRepository
from app.services import CourseService
from app.services import ProductService
from app.services.book_reading_service import BookService
from app.services.book_video_service import BookVideoService
from app.services.instructor_service import InstructorService
from app.services.pathway_service import PathwayService
from app.services.user_service import UserService
from app.services.interactive_course_service import InteractiveCourseService
from app.services.interactive_content_service import InteractiveContentService
from app.services.assist_file_service import AssistFileService
from app.services.assist_image_service import AssistImageService
from app.services.storage_service import StorageService
from app.core.storage import StorageClient

db = Database()

async def get_db_session() -> AsyncGenerator[AsyncSession, Any]:
    async for session in db.get_session():
        yield session


async def get_storage_client() -> AsyncGenerator[StorageClient, Any]:
    yield StorageClient()


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


# Interactive repositories
async def get_interactive_course_details_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[InteractiveCourseDetailsRepository, Any]:
    yield InteractiveCourseDetailsRepository(session)


async def get_interactive_chapter_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[InteractiveChapterRepository, Any]:
    yield InteractiveChapterRepository(session)


async def get_interactive_video_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[InteractiveVideoRepository, Any]:
    yield InteractiveVideoRepository(session)


async def get_interactive_paragraph_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[InteractiveParagraphRepository, Any]:
    yield InteractiveParagraphRepository(session)


async def get_interactive_word_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[InteractiveWordRepository, Any]:
    yield InteractiveWordRepository(session)


async def get_interactive_keyword_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[InteractiveKeyWordRepository, Any]:
    yield InteractiveKeyWordRepository(session)


async def get_file_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[AssistFileRepository, Any]:
    yield AssistFileRepository(session)


async def get_file_type_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[FileTypeRepository, Any]:
    yield FileTypeRepository(session)


async def get_file_image_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[AssistImageRepository, Any]:
    yield AssistImageRepository(session)


async def get_keyword_type_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[KeyWordTypeRepository, Any]:
    yield KeyWordTypeRepository(session)


async def get_word_type_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[WordTypeRepository, Any]:
    yield WordTypeRepository(session)


async def get_video_keyword_type_style_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[VideoKeywordTypeStyleRepository, Any]:
    yield VideoKeywordTypeStyleRepository(session)


async def get_visual_item_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[VisualItemRepository, Any]:
    yield VisualItemRepository(session)


async def get_visual_type_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[VisualTypeRepository, Any]:
    yield VisualTypeRepository(session)


async def get_table_data_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[TableDataRepository, Any]:
    yield TableDataRepository(session)


async def get_chart_data_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[ChartDataRepository, Any]:
    yield ChartDataRepository(session)


async def get_image_repository(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[ImageRepository, Any]:
    yield ImageRepository(session)

async def get_chart_type_repo(
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[ChartTypeRepository, Any]:
    yield ChartTypeRepository(session)

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


async def get_storage_service(
        storage_client: StorageClient = Depends(get_storage_client),
) -> AsyncGenerator[StorageService, Any]:
    yield StorageService(storage_client=storage_client)



async def get_interactive_course_service(
        course_detail_repo: InteractiveCourseDetailsRepository = Depends(get_interactive_course_details_repository),
        chapter_repo: InteractiveChapterRepository = Depends(get_interactive_chapter_repository),
        video_repo: InteractiveVideoRepository = Depends(get_interactive_video_repository),
        product_repo: ProductRepository = Depends(get_product_repository),
        product_skill_repo: ProductSkillRepository = Depends(get_product_skill_repository),
        product_objective_repo: ProductObjectiveRepository = Depends(get_product_objective_repository),
        paragraph_repo: InteractiveParagraphRepository = Depends(get_interactive_paragraph_repository),
        word_repo: InteractiveWordRepository = Depends(get_interactive_word_repository),
        keyword_repo: InteractiveKeyWordRepository = Depends(get_interactive_keyword_repository),
        keyword_type_repo: KeyWordTypeRepository = Depends(get_keyword_type_repository),
        keyword_style_repo: VideoKeywordTypeStyleRepository = Depends(get_video_keyword_type_style_repository),
        visual_repo: VisualItemRepository = Depends(get_visual_item_repository),
        visual_type_repo: VisualTypeRepository = Depends(get_visual_type_repository),
        table_repo: TableDataRepository = Depends(get_table_data_repository),
        chart_repo: ChartDataRepository = Depends(get_chart_data_repository),
        image_repo: ImageRepository = Depends(get_image_repository),
        chart_type_repo: ChartTypeRepository = Depends(get_chart_type_repo),
        file_repo: AssistFileRepository = Depends(get_file_repository),
        storage_service: StorageService = Depends(get_storage_service),
) -> AsyncGenerator["InteractiveCourseService", Any]:
    yield InteractiveCourseService(
        db=course_detail_repo.db,
        course_detail_repo=course_detail_repo,
        chapter_repo=chapter_repo,
        video_repo=video_repo,
        product_repo=product_repo,
        product_skill_repo=product_skill_repo,
        product_objective_repo=product_objective_repo,
        paragraph_repo=paragraph_repo,
        word_repo=word_repo,
        keyword_repo=keyword_repo,
        keyword_type_repo=keyword_type_repo,
        keyword_style_repo=keyword_style_repo,
        visual_repo=visual_repo,
        visual_type_repo=visual_type_repo,
        table_repo=table_repo,
        chart_repo=chart_repo,
        image_repo=image_repo,
        chart_type_repo=chart_type_repo,
        file_repo=file_repo,
        storage_service=storage_service,
    )


async def get_interactive_content_service(
        paragraph_repo: InteractiveParagraphRepository = Depends(get_interactive_paragraph_repository),
        word_type_repo: WordTypeRepository = Depends(get_word_type_repository),
        keyword_repo: InteractiveKeyWordRepository = Depends(get_interactive_keyword_repository),
        keyword_type_repo: KeyWordTypeRepository = Depends(get_keyword_type_repository),
        video_keyword_style_repo: VideoKeywordTypeStyleRepository = Depends(get_video_keyword_type_style_repository),
        visual_repo: VisualItemRepository = Depends(get_visual_item_repository),
        visual_type_repo: VisualTypeRepository = Depends(get_visual_type_repository),
        table_repo: TableDataRepository = Depends(get_table_data_repository),
        chart_repo: ChartDataRepository = Depends(get_chart_data_repository),
        chart_type_repo: ChartTypeRepository = Depends(get_chart_type_repo),
        image_repo: ImageRepository = Depends(get_image_repository),
) -> AsyncGenerator["InteractiveContentService", Any]:
    yield InteractiveContentService(
        db=paragraph_repo.db,
        paragraph_repo=paragraph_repo,
        word_type_repo=word_type_repo,
        keyword_repo=keyword_repo,
        keyword_type_repo=keyword_type_repo,
        video_keyword_style_repo=video_keyword_style_repo,
        visual_repo=visual_repo,
        visual_type_repo=visual_type_repo,
        table_repo=table_repo,
        chart_repo=chart_repo,
        chart_type_repo=chart_type_repo,
        image_repo=image_repo,
    )


async def get_assist_file_service(
        file_repo: AssistFileRepository = Depends(get_file_repository),
        file_type_repo: FileTypeRepository = Depends(get_file_type_repository),
        assist_image_repo: AssistImageRepository = Depends(get_file_image_repository),
        storage_service: StorageService = Depends(get_storage_service),
) -> AsyncGenerator["AssistFileService", Any]:
    yield AssistFileService(
        db=file_repo.db,
        file_repo=file_repo,
        file_type_repo=file_type_repo,
        assist_image_repo=assist_image_repo,
        storage_service=storage_service,
    )


async def get_assist_image_service(
        image_repo: AssistImageRepository = Depends(get_file_image_repository),
        storage_service: StorageService = Depends(get_storage_service),
) -> AsyncGenerator["AssistImageService", Any]:
    yield AssistImageService(
        db=image_repo.db,
        image_repo=image_repo,
        storage_service=storage_service,
    )
