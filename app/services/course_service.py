import uuid
from typing import Sequence, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CourseDetail
from app.repositories import (
    CourseDetailRepository,
    ChapterRepository,
    VideoRepository,
    ProductRepository,
    ProductObjectiveRepository,
    ProductRatingRepository,
    ProductSkillRepository,
    CourseInstructorRepository,
)
from app.schemas.course import CourseDetailSchema


class CourseService:
    def __init__(
            self,
            db: AsyncSession,
            course_detail_repo: CourseDetailRepository,
            chapter_repo: ChapterRepository,
            video_repo: VideoRepository,
            product_repo: ProductRepository,
            product_skill_repo: ProductSkillRepository,
            product_objective_repo: ProductObjectiveRepository,
            course_instructor_repo: CourseInstructorRepository,
            product_rating_repo: ProductRatingRepository,
    ):
        self.db = db
        self.course_detail_repo = course_detail_repo
        self.chapter_repo = chapter_repo
        self.video_repo = video_repo
        self.product_repo = product_repo
        self.product_skill_repo = product_skill_repo
        self.product_objective_repo = product_objective_repo
        self.course_instructor_repo = course_instructor_repo
        self.product_rating_repo = product_rating_repo

    async def create_course_product(self, course_data: CourseDetailSchema) -> uuid.UUID:
        """
        Create a new course product along with chapters, videos,
        skills, objectives, instructors, and assessments.
        All operations are executed in a single transaction.
        """
        async with self.db.begin():  # ✅ ensures atomic transaction
            # 1. Create Product
            product = await self.product_repo.create({
                "type_id": course_data.product_type_id,
                "category_id": course_data.product_category_id,
                "title": course_data.title,
                "description": course_data.description,
                "language": course_data.language,
                "level": course_data.level,
                "duration": course_data.duration,
            })

            # 2. Create CourseDetail
            course_detail = await self.course_detail_repo.create({
                "product_id": product.id,
                "video_count": sum(len(ch.videos) for ch in course_data.chapters),
                "total_hours": course_data.total_hours or 0,
                "students_count": course_data.students_count or 0,
                "certificate_included": course_data.certificate_included,
                "pre_assessment_id": course_data.pre_assessment_id,
                "final_exam_id": course_data.final_exam_id,
                "about": course_data.about,
            })

            # 3. Create Chapters and Videos
            for chapter_index, chapter in enumerate(course_data.chapters):
                chapter_obj = await self.chapter_repo.create({
                    "course_id": course_detail.id,
                    "title": chapter.title,
                    "description": chapter.description,
                    "about": chapter.about,
                    "view_index": chapter_index + 1,
                    "quiz_id": chapter.quiz_id,
                })

                for video_index, video in enumerate(chapter.videos):
                    await self.video_repo.create({
                        "chapter_id": chapter_obj.id,
                        "title": video.title,
                        "url": video.url,
                        "video_duration": video.video_duration,
                        "view_index": video_index + 1,
                        "quiz_id": video.quiz_id,
                    })

            # 4. Add Skills (many-to-many)
            if course_data.skills:
                for skill_id in course_data.skills:
                    await self.product_skill_repo.create({
                        "product_id": product.id,
                        "skill_id": skill_id,
                    })

            # 5. Add Objectives (many-to-many)
            if course_data.objectives:
                for obj_id in course_data.objectives:
                    await self.product_objective_repo.create({
                        "product_id": product.id,
                        "objective_id": obj_id,
                    })

            # 6. Add Instructors (many-to-many)
            if course_data.instructors:
                for instructor_id in course_data.instructors:
                    await self.course_instructor_repo.create({
                        "course_id": course_detail.id,
                        "instructor_id": instructor_id,
                    })

        # ✅ Transaction committed if no error
        return product.id

    async def get_course_product(self, product_id: uuid.UUID) -> CourseDetail | None:
        """
        Fetch a course by product ID, including chapters and videos.
        """
        return await self.course_detail_repo.get_course_product(product_id)

    async def get_all_courses(
            self, page: int = 1, limit: int = 10, category_id: Optional[uuid.UUID] = None,
    ) -> Sequence[CourseDetail]:
        """
        Fetch all courses with optional pagination.
        """
        return await self.course_detail_repo.get_all_course_product(
            page=page, limit=limit, category_id=category_id
        )

    async def delete_course_product(self, product_id: uuid.UUID) -> bool:
        """
        Delete a course product by its product ID.
        This will also cascade delete associated course details, chapters, and videos.
        """
        async with self.db.begin():
            return await self.product_repo.delete(product_id)


    async def get_product_rating(self, product_id: uuid.UUID) -> float | None:
        """
        Get the average rating for a product.
        """
        return await self.product_rating_repo.get_product_rating(product_id)
