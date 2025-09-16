import uuid
from typing import Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exception import CustomException
from app.exceptions.service_exception import ServiceException
from app.models.interactive_models.interactive_course_details_model import InteractiveCourseDetailsModel
from app.repositories.interactive_repositories import (
    InteractiveCourseDetailsRepository,
    InteractiveChapterRepository,
    InteractiveVideoRepository,
)
from app.repositories.product import ProductRepository
from app.repositories.skill import ProductSkillRepository
from app.repositories import ProductObjectiveRepository
from app.schemas.interactive_schemas import (
    InteractiveCourseCreateSchema,
    InteractiveCourseUpdateSchema,
)
from app.constant_manager import ProductType
from app.schemas.interactive_schemas.interactive_course_schema import InteractiveChapterCreateSchema, InteractiveChapterUpdateSchema


class InteractiveCourseService:
    def __init__(
            self,
            db: AsyncSession,
            course_detail_repo: InteractiveCourseDetailsRepository,
            chapter_repo: InteractiveChapterRepository,
            video_repo: InteractiveVideoRepository,
            product_repo: ProductRepository,
            product_skill_repo: ProductSkillRepository,
            product_objective_repo: ProductObjectiveRepository,
    ):
        self.db = db
        self.course_detail_repo = course_detail_repo
        self.chapter_repo = chapter_repo
        self.video_repo = video_repo
        self.product_repo = product_repo
        self.product_skill_repo = product_skill_repo
        self.product_objective_repo = product_objective_repo

    async def create_interactive_course_product(self, course_data: InteractiveCourseCreateSchema) -> dict[str, uuid.UUID]:
        """
        Create a new interactive course product along with chapters, videos,
        skills, and objectives.
        All operations are executed in a single transaction.
        """
        try:
            async with self.db.begin():
                # 1. Create Product
                product = await self.product_repo.create({
                    "type_id": ProductType.INTERACTIVE_COURSES_ID,
                    "category_id": course_data.category_id,
                    "title": course_data.title,
                    "description": course_data.description,
                    "language": course_data.language,
                    "level_id": course_data.level_id,
                    "cover": course_data.cover,
                    "short_video": course_data.short_video,
                    "created_by": course_data.created_by,
                    "duration": course_data.duration,
                })

                # 2. Create Interactive Course Detail
                course_detail = await self.course_detail_repo.create({
                    "product_id": product.id,
                    "pre_assessment_id": course_data.pre_assessment_id,
                    "final_exam_id": course_data.final_exam_id,
                })

                # 3. Create Chapters and Videos
                if course_data.chapters:
                    for chapter_data in course_data.chapters:
                        await self.chapter_repo.create({
                            "course_id": course_detail.id,
                            "title": chapter_data.title,
                            "description": chapter_data.description,
                            "about": chapter_data.about,
                            "view_index": chapter_data.view_index,
                            "quiz_id": chapter_data.quiz_id,
                        })

                        # Create videos for chapter
                        # for video_data in chapter_data.videos:
                        #     await self.video_repo.create({
                        #         "chapter_id": chapter_obj.id,
                        #         "title": video_data.title,
                        #         "url": video_data.url,
                        #         "video_duration": video_data.video_duration,
                        #         "view_index": video_data.view_index or 0,
                        #         "quiz_id": video_data.quiz_id,
                        #     })

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

            return {"course_id": course_detail.id, "product_id": product.id,}

        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create interactive course product",
                additional_info={"error": str(e)},
            )

    async def get_interactive_course_product(self, product_id: uuid.UUID) -> dict[str, Any] | None:
        """
        Fetch an interactive course by product ID, including chapters and videos.
        """
        try:
            return await self.course_detail_repo.get_interactive_course_product(product_id)
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch interactive course product",
                additional_info={"error": str(e), "product_id": str(product_id)},
            )

    async def get_all_interactive_courses(
            self, 
            page: int = 1, 
            limit: int = 10,
            category_id: Optional[uuid.UUID] = None,
            skill_id: Optional[uuid.UUID] = None
    ) -> list[dict[str, Any]]:
        """
        Fetch all interactive courses with optional pagination.
        """
        try:
            return await self.course_detail_repo.get_all_interactive_course_product(
                page=page, 
                limit=limit,
                category_id=category_id,
                skill_id=skill_id
            )
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch all interactive courses",
                additional_info={
                    "error": str(e),
                    "page": page,
                    "limit": limit,
                    "category_id": str(category_id) if category_id else None,
                    "skill_id": str(skill_id) if skill_id else None,
                },
            )

    async def update_interactive_course_product(
            self, 
            product_id: uuid.UUID, 
            course_update: InteractiveCourseUpdateSchema
    ) -> bool:
        """
        Update an interactive course product by its product ID.
        """
        try:
            async with self.db.begin():
                # Update the product
                product_update_data = {}
                
                # Only include fields that are provided
                if course_update.category_id is not None:
                    product_update_data["category_id"] = course_update.category_id
                if course_update.level_id is not None:
                    product_update_data["level_id"] = course_update.level_id
                if course_update.title is not None:
                    product_update_data["title"] = course_update.title
                if course_update.description is not None:
                    product_update_data["description"] = course_update.description
                if course_update.language is not None:
                    product_update_data["language"] = course_update.language
                if course_update.duration is not None:
                    product_update_data["duration"] = course_update.duration
                if course_update.cover is not None:
                    product_update_data["cover"] = course_update.cover
                if course_update.short_video is not None:
                    product_update_data["short_video"] = course_update.short_video
                
                if product_update_data:
                    product = await self.product_repo.update(product_id, product_update_data)
                    if not product:
                        raise ServiceException(
                            status_code=404,
                            detail="Product not found",
                            additional_info={"product_id": str(product_id)},
                        )
                
                # Update interactive course details
                course_update_data = {}
                
                if course_update.pre_assessment_id is not None:
                    course_update_data["pre_assessment_id"] = course_update.pre_assessment_id
                if course_update.final_exam_id is not None:
                    course_update_data["final_exam_id"] = course_update.final_exam_id
                
                if course_update_data:
                    # Get the interactive course detail by product_id
                    result = await self.course_detail_repo.get_interactive_course_product(product_id)
                    if not result:
                        raise ServiceException(
                            status_code=404,
                            detail="Interactive course not found",
                            additional_info={"product_id": str(product_id)},
                        )
                    
                    # Update using the course detail ID
                    course_detail = result["product"].interactive_course_detail
                    await self.course_detail_repo.update(course_detail.id, course_update_data)

                # Update Skills (many-to-many) - Replace existing skills
                if course_update.skills is not None:
                    # First, remove existing skills
                    existing_skills = await self.product_skill_repo.get_skills_by_product_id(product_id)
                    for skill_relation in existing_skills:
                        await self.product_skill_repo.delete(skill_relation.id)
                    
                    # Add new skills
                    for skill_id in course_update.skills:
                        await self.product_skill_repo.create({
                            "product_id": product_id,
                            "skill_id": skill_id,
                        })

                # Update Objectives (many-to-many) - Replace existing objectives
                if course_update.objectives is not None:
                    # First, remove existing objectives
                    existing_objectives = await self.product_objective_repo.get_objectives_by_product_id(product_id)
                    for objective_relation in existing_objectives:
                        await self.product_objective_repo.delete(objective_relation.id)
                    
                    # Add new objectives
                    for obj_id in course_update.objectives:
                        await self.product_objective_repo.create({
                            "product_id": product_id,
                            "objective_id": obj_id,
                        })
                
                return True

        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to update interactive course product",
                additional_info={"error": str(e), "product_id": str(product_id)},
            )

    async def get_course_detail_by_product_id(self, product_id: uuid.UUID) -> uuid.UUID:
        """
        Get the interactive course detail ID from a product ID.
        Raises ServiceException if not found.
        """
        try:
            result = await self.course_detail_repo.get_interactive_course_product(product_id)
            if not result:
                raise ServiceException(
                    status_code=404,
                    detail="Interactive course not found",
                    additional_info={"product_id": str(product_id)},
                )
            return result["product"].interactive_course_detail.id
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to get course detail ID",
                additional_info={"error": str(e), "product_id": str(product_id)},
            )

    async def create_chapter(self, chapter_data: InteractiveChapterCreateSchema) -> dict:
        """
        Create a new chapter for an interactive course.
        """
        try:
            async with self.db.begin():
                chapter = await self.chapter_repo.create(chapter_data.model_dump())
                await self.db.flush()
                chapter_dict = {
                    "id": chapter.id,
                    "course_id": chapter.course_id,
                    "title": chapter.title,
                    "description": chapter.description,
                    "about": chapter.about,
                    "view_index": chapter.view_index,
                    "quiz_id": chapter.quiz_id,
                }
            return chapter_dict
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create chapter",
                additional_info={"error": str(e), "chapter_data": chapter_data},
            )

    async def create_video(self, video_data: dict) -> dict:
        """
        Create a new video for an interactive chapter.
        """
        try:
            async with self.db.begin():
                video = await self.video_repo.create(video_data)
            return video
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create video",
                additional_info={"error": str(e), "video_data": video_data},
            )

    async def update_chapter(self, chapter_id: uuid.UUID, chapter_data: InteractiveChapterUpdateSchema) -> dict:
        """
        Update an existing chapter.
        """
        try:
            async with self.db.begin():
                update_data = {}
                if chapter_data.title is not None:
                    update_data["title"] = chapter_data.title
                if chapter_data.description is not None:
                    update_data["description"] = chapter_data.description
                if chapter_data.about is not None:
                    update_data["about"] = chapter_data.about
                if chapter_data.view_index is not None:
                    update_data["view_index"] = chapter_data.view_index
                if chapter_data.quiz_id is not None:
                    update_data["quiz_id"] = chapter_data.quiz_id
                
                if not update_data:
                    raise ServiceException(
                        status_code=400,
                        detail="No fields to update",
                        additional_info={"chapter_id": str(chapter_id)},
                    )
                
                chapter = await self.chapter_repo.update(chapter_id, update_data)
                if not chapter:
                    raise ServiceException(
                        status_code=404,
                        detail="Chapter not found",
                        additional_info={"chapter_id": str(chapter_id)},
                    )
                
                await self.db.flush()
                chapter_dict = {
                    "id": chapter.id,
                    "course_id": chapter.course_id,
                    "title": chapter.title,
                    "description": chapter.description,
                    "about": chapter.about,
                    "view_index": chapter.view_index,
                    "quiz_id": chapter.quiz_id,
                }
            return chapter_dict
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to update chapter",
                additional_info={"error": str(e), "chapter_id": str(chapter_id)},
            )

    async def delete_chapter(self, chapter_id: uuid.UUID) -> bool:
        """
        Delete a chapter by its ID.
        This will also cascade delete associated videos.
        """
        try:
            async with self.db.begin():
                success = await self.chapter_repo.delete(chapter_id)
                if not success:
                    raise ServiceException(
                        status_code=404,
                        detail="Chapter not found",
                        additional_info={"chapter_id": str(chapter_id)},
                    )
            return success
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to delete chapter",
                additional_info={"error": str(e), "chapter_id": str(chapter_id)},
            )

    async def delete_interactive_course_product(self, product_id: uuid.UUID) -> bool:
        """
        Delete an interactive course product by its product ID.
        This will also cascade delete associated course details, chapters, and videos.
        """
        try:
            async with self.db.begin():
                success = await self.product_repo.delete(product_id)
                if not success:
                    raise ServiceException(
                        status_code=404,
                        detail="Interactive course not found",
                        additional_info={"product_id": str(product_id)},
                    )
                return success
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to delete interactive course product",
                additional_info={"error": str(e), "product_id": str(product_id)},
            )