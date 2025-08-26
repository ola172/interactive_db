import uuid
from datetime import datetime
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CourseDetail, CourseCategory
from app.repositories import (
    CourseDetailRepository,
    ChapterRepository,
    VideoRepository,
    ProductRepository,
    CourseCategoryRepository,
)
from app.schemas.course import CreateCourse, CourseCategoryBase


class CourseService:
    def __init__(
        self,
        db: AsyncSession,
        course_detail_repo: CourseDetailRepository,
        chapter_repo: ChapterRepository,
        video_repo: VideoRepository,
        course_category_repo: CourseCategoryRepository,
        product_repo: ProductRepository,
    ):
        self.db = db
        self.course_detail_repo = course_detail_repo
        self.chapter_repo = chapter_repo
        self.video_repo = video_repo
        self.product_repo = product_repo
        self.course_category_repo = course_category_repo

    async def get_all_course_categories(
        self, page: int = 1, limit: int = 10
    ) -> Sequence[CourseCategory]:
        """
        Fetch all course categories with optional pagination.
        """
        return await self.course_category_repo.get_all(page=page, limit=limit)

    async def create_course_category(
        self, course_category: CourseCategoryBase
    ) -> CourseCategory:
        """
        Create a new course category.
        Only fields defined in the model are used.
        """
        category_data = {
            "name": course_category.name,
            "description": course_category.description
        }
        async with self.db.begin():
            category = await self.course_category_repo.create(category_data)
        return category

    async def create_course_product(self, course_data: CreateCourse) -> uuid.UUID:
        """
        Create a new course product along with chapters and videos.
        All operations are executed in a single transaction.
        """
        async with self.db.begin():  # Transaction block ensures atomicity
            # Create Product
            product = await self.product_repo.create({
                "type_id": course_data.product_type_id,
                "title": course_data.title,
                "description": course_data.description,
                "language": course_data.language,
                "level": course_data.level,
                "duration": course_data.duration,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })

            # Create CourseDetail
            course_detail = await self.course_detail_repo.create({
                "product_id": product.id,
                "video_count": 20,
                "total_hours": 50,
                "students_count": 0,
                "certificate_included": course_data.certificate_included
            })

            # Create Chapters and Videos with order indexing
            for chapter_index, chapter in enumerate(course_data.chapters):
                chapter_obj = await self.chapter_repo.create({
                    "course_id": course_detail.id,
                    "title": chapter.title,
                    "description": chapter.description,
                    "order_index": chapter_index + 1
                })

                for video_index, video in enumerate(chapter.videos):
                    await self.video_repo.create({
                        "chapter_id": chapter_obj.id,
                        "title": video.title,
                        "url": video.url,
                        "order_index": video_index + 1
                    })

        # Transaction automatically committed if no exception occurs
        return product.id

    async def get_course_product(self, product_id: uuid.UUID) -> CourseDetail | None:
        """
        Fetch a course by product ID, including chapters and videos.
        """
        return await self.course_detail_repo.get_course_product(product_id)

    async def get_all_courses(
        self, page: int = 1, limit: int = 10
    ) -> Sequence[CourseDetail]:
        """
        Fetch all courses with optional pagination.
        """
        return await self.course_detail_repo.get_all_course_product(
            page=page, limit=limit
        )

