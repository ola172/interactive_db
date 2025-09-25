import uuid
from typing import Optional, Any, List
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exception import CustomException
from app.exceptions.service_exception import ServiceException
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
    ChartTypeRepository,
    ImageRepository,
)
from app.repositories.interactive_repositories.file_repository import FileRepository
from app.services.storage_service import StorageService
from app.repositories.product import ProductRepository
from app.repositories.skill import ProductSkillRepository
from app.repositories import ProductObjectiveRepository
from app.schemas.interactive_schemas import (
    InteractiveCourseCreateSchema,
    InteractiveCourseUpdateSchema,
)
from app.constant_manager import ProductType, StorageBucket
from app.schemas.interactive_schemas import (
    InteractiveChapterCreateSchema,
    InteractiveChapterUpdateSchema,
    InteractiveVideoCreateSchema,
    InteractiveVideoUpdateSchema,
    InteractiveVideoUploadSchema,
    VideoKeywordStyleUpdateSchema,
    VideoKeywordTypeStyleUpdateSchema,
    VisualDataCreateSchema,
    VisualDataUpdateSchema,
)
from app.helper import VisualDataRegistry


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
        paragraph_repo: InteractiveParagraphRepository,
        word_repo: InteractiveWordRepository,
        keyword_repo: InteractiveKeyWordRepository,
        keyword_type_repo: KeyWordTypeRepository,
        keyword_style_repo: VideoKeywordTypeStyleRepository,
        visual_repo: VisualItemRepository,
        visual_type_repo: VisualTypeRepository,
        table_repo: TableDataRepository,
        chart_repo: ChartDataRepository,
        chart_type_repo: ChartTypeRepository,
        image_repo: ImageRepository,
        file_repo: FileRepository,
        storage_service: StorageService,
    ):
        self.db = db
        self.course_detail_repo = course_detail_repo
        self.chapter_repo = chapter_repo
        self.video_repo = video_repo
        self.product_repo = product_repo
        self.product_skill_repo = product_skill_repo
        self.product_objective_repo = product_objective_repo
        self.paragraph_repo = paragraph_repo
        self.word_repo = word_repo
        self.keyword_repo = keyword_repo
        self.keyword_type_repo = keyword_type_repo
        self.keyword_style_repo = keyword_style_repo
        self.visual_repo = visual_repo
        self.visual_type_repo = visual_type_repo
        self.table_repo = table_repo
        self.chart_repo = chart_repo
        self.chart_type_repo = chart_type_repo
        self.image_repo = image_repo
        self.file_repo = file_repo
        self.storage_service = storage_service

        # Initialize visual data registry
        self.visual_registry = VisualDataRegistry()

    async def _create_visual_data_with_registry(
        self, paragraph_id: uuid.UUID, visual_data: VisualDataCreateSchema
    ) -> dict:
        """Create visual data using registry pattern to determine handler based on visual_type_id."""
        # Get visual type by ID
        visual_type = await self.visual_type_repo.get(visual_data.visual_type_id)
        if not visual_type:
            raise ServiceException(
                status_code=400,
                detail="Visual type not found",
                additional_info={"visual_type_id": str(visual_data.visual_type_id)},
            )

        # Get the appropriate handler for this visual type
        handler = self.visual_registry.get_handler(visual_type.name)

        # Prepare repositories for handler
        repos = {
            "table_repo": self.table_repo,
            "chart_repo": self.chart_repo,
            "image_repo": self.image_repo,
        }

        # Determine which data to use based on visual type
        data_to_use = {}
        if visual_type.name == "table" and visual_data.table_data:
            data_to_use = visual_data.table_data.model_dump()
        elif visual_type.name == "chart" and visual_data.chart_data:
            data_to_use = visual_data.chart_data.model_dump()
        elif visual_type.name == "image" and visual_data.image_data:
            data_to_use = visual_data.image_data.model_dump()
        else:
            raise ServiceException(
                status_code=400,
                detail=f"No {visual_type.name} data provided for {visual_type.name} visual type",
                additional_info={"visual_type": visual_type.name},
            )

        # Create the specific data using the handler
        specific_data_id = await handler.create(data_to_use, repos)

        # Create visual item linking to the specific data
        visual_dict = {
            "visual_type_id": visual_data.visual_type_id,
            "paragraph_id": paragraph_id,
            "start_time": visual_data.start_time,
            "table_id": (specific_data_id if visual_type.name == "table" else None),
            "chart_id": (specific_data_id if visual_type.name == "chart" else None),
            "image_id": (specific_data_id if visual_type.name == "image" else None),
        }
        visual_item = await self.visual_repo.create(visual_dict)

        # Link assist image if provided
        if visual_data.assist_image_id:
            await self._link_assist_image_to_visual_item(
                visual_data.assist_image_id, visual_item.id
            )

        return {
            "id": visual_item.id,
            "visual_type_id": visual_item.visual_type_id,
            "paragraph_id": visual_item.paragraph_id,
            "start_time": visual_item.start_time,
            "table_id": visual_item.table_id,
            "chart_id": visual_item.chart_id,
            "image_id": visual_item.image_id,
            "assist_image_id": visual_data.assist_image_id,
        }

    async def create_interactive_course_product(
        self, course_data: InteractiveCourseCreateSchema
    ) -> dict[str, uuid.UUID]:
        """
        Create a new interactive course product along with chapters, videos,
        skills, and objectives.
        All operations are executed in a single transaction.
        """
        try:
            async with self.db.begin():
                # 1. Create Product
                product = await self.product_repo.create(
                    {
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
                    }
                )

                # 2. Create Interactive Course Detail
                course_detail = await self.course_detail_repo.create(
                    {
                        "product_id": product.id,
                        "pre_assessment_id": course_data.pre_assessment_id,
                        "final_exam_id": course_data.final_exam_id,
                    }
                )

                # 3. Create Chapters and Videos
                if course_data.chapters:
                    for chapter_data in course_data.chapters:
                        await self.chapter_repo.create(
                            {
                                "course_id": course_detail.id,
                                "title": chapter_data.title,
                                "description": chapter_data.description,
                                "about": chapter_data.about,
                                "view_index": chapter_data.view_index,
                                "quiz_id": chapter_data.quiz_id,
                            }
                        )

                # 4. Add Skills (many-to-many)
                if course_data.skills:
                    for skill_id in course_data.skills:
                        await self.product_skill_repo.create(
                            {
                                "product_id": product.id,
                                "skill_id": skill_id,
                            }
                        )

                # 5. Add Objectives (many-to-many)
                if course_data.objectives:
                    for obj_id in course_data.objectives:
                        await self.product_objective_repo.create(
                            {
                                "product_id": product.id,
                                "objective_id": obj_id,
                            }
                        )

            return {
                "course_id": course_detail.id,
                "product_id": product.id,
            }

        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create interactive course product",
                additional_info={"error": str(e)},
            )

    async def get_interactive_course_product(
        self, product_id: uuid.UUID
    ) -> dict[str, Any] | None:
        """
        Fetch an interactive course by product ID, including chapters and videos.
        """
        try:
            return await self.course_detail_repo.get_interactive_course_product(
                product_id
            )
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
        skill_id: Optional[uuid.UUID] = None,
    ) -> list[dict[str, Any]]:
        """
        Fetch all interactive courses with optional pagination.
        """
        try:
            return await self.course_detail_repo.get_all_interactive_course_product(
                page=page, limit=limit, category_id=category_id, skill_id=skill_id
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
        self, product_id: uuid.UUID, course_update: InteractiveCourseUpdateSchema
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
                    product = await self.product_repo.update(
                        product_id, product_update_data
                    )
                    if not product:
                        raise ServiceException(
                            status_code=404,
                            detail="Product not found",
                            additional_info={"product_id": str(product_id)},
                        )

                # Update interactive course details
                course_update_data = {}

                if course_update.pre_assessment_id is not None:
                    course_update_data["pre_assessment_id"] = (
                        course_update.pre_assessment_id
                    )
                if course_update.final_exam_id is not None:
                    course_update_data["final_exam_id"] = course_update.final_exam_id

                if course_update_data:
                    # Get the interactive course detail by product_id
                    result = (
                        await self.course_detail_repo.get_interactive_course_product(
                            product_id
                        )
                    )
                    if not result:
                        raise ServiceException(
                            status_code=404,
                            detail="Interactive course not found",
                            additional_info={"product_id": str(product_id)},
                        )

                    # Update using the course detail ID
                    course_detail = result["product"].interactive_course_detail
                    await self.course_detail_repo.update(
                        course_detail.id, course_update_data
                    )

                # Update Skills (many-to-many) - Replace existing skills
                if course_update.skills is not None:
                    # First, remove existing skills
                    existing_skills = (
                        await self.product_skill_repo.get_skills_by_product_id(
                            product_id
                        )
                    )
                    for skill_relation in existing_skills:
                        await self.product_skill_repo.delete(skill_relation.id)

                    # Add new skills
                    for skill_id in course_update.skills:
                        await self.product_skill_repo.create(
                            {
                                "product_id": product_id,
                                "skill_id": skill_id,
                            }
                        )

                # Update Objectives (many-to-many) - Replace existing objectives
                if course_update.objectives is not None:
                    # First, remove existing objectives
                    existing_objectives = (
                        await self.product_objective_repo.get_objectives_by_product_id(
                            product_id
                        )
                    )
                    for objective_relation in existing_objectives:
                        await self.product_objective_repo.delete(objective_relation.id)

                    # Add new objectives
                    for obj_id in course_update.objectives:
                        await self.product_objective_repo.create(
                            {
                                "product_id": product_id,
                                "objective_id": obj_id,
                            }
                        )

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
            result = await self.course_detail_repo.get_interactive_course_product(
                product_id
            )
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

    async def create_chapter(
        self, chapter_data: InteractiveChapterCreateSchema
    ) -> dict:
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

    async def create_video(self, video_data: InteractiveVideoCreateSchema) -> dict:
        """
        Create a new video for an interactive chapter with all paragraphs data,
        words, keywords, visual data, and keyword type styles.
        """
        try:
            async with self.db.begin():
                # 1. Create video
                video_dict = {
                    "chapter_id": video_data.chapter_id,
                    "quiz_id": video_data.quiz_id,
                    "title": video_data.title,
                    "url": video_data.url,
                    "video_duration": video_data.video_duration,
                    "view_index": video_data.view_index,
                }
                video = await self.video_repo.create(video_dict)
                await self.db.flush()

                # 2. Create default keyword type styles for this video
                # Get all available keyword types and create default styles for each
                all_keyword_types = await self.keyword_type_repo.get_all(
                    page=1, limit=1000
                )
                for keyword_type in all_keyword_types:
                    style_dict = {
                        "video_id": video.id,
                        "keyword_type_id": keyword_type.id,
                        "color_light": "#000000",  # Default black for light theme
                        "color_dark": "#FFFFFF",  # Default white for dark theme
                        "shadow_light": None,  # No shadow by default
                        "shadow_dark": None,  # No shadow by default
                        "size": 14,  # Default font size
                    }
                    await self.keyword_style_repo.create(style_dict)

                # 3. Create paragraphs with their content
                for paragraph_data in video_data.paragraphs:
                    # Create paragraph
                    paragraph_dict = {
                        "video_id": video.id,
                        "view_index": paragraph_data.view_index,
                        "paragraph_text": paragraph_data.paragraph_text,
                        "start_time": paragraph_data.start_time,
                        "end_time": paragraph_data.end_time,
                    }
                    paragraph = await self.paragraph_repo.create(paragraph_dict)
                    await self.db.flush()

                    # Create words for this paragraph
                    for word_data in paragraph_data.words:
                        word_dict = {
                            "paragraph_id": paragraph.id,
                            "type_id": word_data.word_type_id,
                            "word": word_data.word,
                            "start_time": word_data.start_time,
                            "end_time": word_data.end_time,
                        }
                        await self.word_repo.create(word_dict)

                    # Create keywords for this paragraph
                    for keyword_data in paragraph_data.keywords:
                        keyword_dict = {
                            "paragraph_id": paragraph.id,
                            "type_id": keyword_data.keyword_type_id,
                            "word": keyword_data.word,
                        }
                        await self.keyword_repo.create(keyword_dict)

                    # Create visual data if present
                    if paragraph_data.visual_data:
                        await self._create_visual_data_with_registry(
                            paragraph.id, paragraph_data.visual_data
                        )

                video_data = await self.video_repo.get_video_with_paragraphs(
                    video_id=video.id
                )
            return video_data
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create video",
                additional_info={"error": str(e), "video_data": str(video_data)},
            )

    async def update_video(
        self, video_id: uuid.UUID, video_data: InteractiveVideoUpdateSchema
    ) -> dict:
        """
        Update an existing video metadata (not paragraphs).
        """
        try:
            async with self.db.begin():
                update_data = {}
                if video_data.title is not None:
                    update_data["title"] = video_data.title
                if video_data.url is not None:
                    update_data["url"] = video_data.url
                if video_data.video_duration is not None:
                    update_data["video_duration"] = video_data.video_duration
                if video_data.view_index is not None:
                    update_data["view_index"] = video_data.view_index
                if video_data.quiz_id is not None:
                    update_data["quiz_id"] = video_data.quiz_id

                if not update_data:
                    raise ServiceException(
                        status_code=400,
                        detail="No fields to update",
                        additional_info={"video_id": str(video_id)},
                    )

                video = await self.video_repo.update(video_id, update_data)
                if not video:
                    raise ServiceException(
                        status_code=404,
                        detail="Video not found",
                        additional_info={"video_id": str(video_id)},
                    )

                await self.db.flush()
                video_response = {
                    "id": video.id,
                    "chapter_id": video.chapter_id,
                    "quiz_id": video.quiz_id,
                    "title": video.title,
                    "url": video.url,
                    "video_duration": video.video_duration,
                    "view_index": video.view_index,
                }
            return video_response
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to update video",
                additional_info={"error": str(e), "video_id": str(video_id)},
            )

    async def delete_video(self, video_id: uuid.UUID) -> bool:
        """
        Delete a video by its ID.
        This will also cascade delete associated paragraphs, words, keywords, and visual data.
        """
        try:
            async with self.db.begin():
                success = await self.video_repo.delete(video_id)
                if not success:
                    raise ServiceException(
                        status_code=404,
                        detail="Video not found",
                        additional_info={"video_id": str(video_id)},
                    )
            return success
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to delete video",
                additional_info={"error": str(e), "video_id": str(video_id)},
            )

    async def update_chapter(
        self, chapter_id: uuid.UUID, chapter_data: InteractiveChapterUpdateSchema
    ) -> dict:
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

    async def update_video_keyword_type_style(
        self,
        video_id: uuid.UUID,
        keyword_type_id: uuid.UUID,
        style_data: VideoKeywordTypeStyleUpdateSchema,
    ) -> dict:
        """
        Update the style for a specific keyword type in a video.
        """
        try:
            async with self.db.begin():
                # Check if the style exists
                existing_style = (
                    await self.keyword_style_repo.get_style_by_video_and_type(
                        video_id, keyword_type_id
                    )
                )
                if not existing_style:
                    raise ServiceException(
                        status_code=404,
                        detail="Video keyword type style not found",
                        additional_info={
                            "video_id": str(video_id),
                            "keyword_type_id": str(keyword_type_id),
                        },
                    )

                # Prepare update data - only include non-None values
                update_data = {}
                if style_data.color_light is not None:
                    update_data["color_light"] = style_data.color_light
                if style_data.color_dark is not None:
                    update_data["color_dark"] = style_data.color_dark
                if style_data.shadow_light is not None:
                    update_data["shadow_light"] = style_data.shadow_light
                if style_data.shadow_dark is not None:
                    update_data["shadow_dark"] = style_data.shadow_dark
                if style_data.size is not None:
                    update_data["size"] = style_data.size

                if not update_data:
                    raise ServiceException(
                        status_code=400,
                        detail="No fields to update",
                        additional_info={
                            "video_id": str(video_id),
                            "keyword_type_id": str(keyword_type_id),
                        },
                    )

                # Update the style
                updated_style = await self.keyword_style_repo.update(
                    existing_style.id, update_data
                )

                await self.db.flush()
                style_response = {
                    "id": updated_style.id,
                    "video_id": updated_style.video_id,
                    "keyword_type_id": updated_style.keyword_type_id,
                    "color_light": updated_style.color_light,
                    "color_dark": updated_style.color_dark,
                    "shadow_light": updated_style.shadow_light,
                    "shadow_dark": updated_style.shadow_dark,
                    "size": updated_style.size,
                }
            return style_response
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to update video keyword type style",
                additional_info={
                    "error": str(e),
                    "video_id": str(video_id),
                    "keyword_type_id": str(keyword_type_id),
                },
            )

    async def create_visual_data(
        self, paragraph_id: uuid.UUID, visual_data: VisualDataCreateSchema
    ) -> dict:
        """
        Create visual data using registry pattern to determine handler based on visual_type_id.
        """
        try:
            async with self.db.begin():
                return await self._create_visual_data_with_registry(paragraph_id, visual_data)
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create visual data",
                additional_info={"error": str(e), "paragraph_id": str(paragraph_id)},
            )

    async def update_visual_data(
        self, visual_id: uuid.UUID, visual_data: VisualDataUpdateSchema
    ) -> dict:
        """
        Update visual data using registry pattern.
        """
        try:
            async with self.db.begin():
                # Get existing visual item
                visual_item = await self.visual_repo.get(visual_id)
                if not visual_item:
                    raise ServiceException(
                        status_code=404,
                        detail="Visual item not found",
                        additional_info={"visual_id": str(visual_id)},
                    )

                # Update visual item basic fields
                visual_update_data = {}
                if visual_data.visual_type_id is not None:
                    visual_update_data["visual_type_id"] = visual_data.visual_type_id
                if visual_data.start_time is not None:
                    visual_update_data["start_time"] = visual_data.start_time

                if visual_update_data:
                    visual_item = await self.visual_repo.update(visual_id, visual_update_data)

                # Get visual type to determine handler
                visual_type = await self.visual_type_repo.get(visual_item.visual_type_id)
                if not visual_type:
                    raise ServiceException(
                        status_code=400,
                        detail="Visual type not found",
                        additional_info={"visual_type_id": str(visual_item.visual_type_id)},
                    )

                # Update specific data if provided
                handler = self.visual_registry.get_handler(visual_type.name)
                repos = {
                    "table_repo": self.table_repo,
                    "chart_repo": self.chart_repo,
                    "image_repo": self.image_repo,
                }

                # Update the specific data based on type
                if (
                    visual_type.name == "table"
                    and visual_data.table_data
                    and visual_item.table_id
                ):
                    await handler.update(
                        visual_item.table_id,
                        visual_data.table_data.model_dump(),
                        repos,
                    )
                elif (
                    visual_type.name == "chart"
                    and visual_data.chart_data
                    and visual_item.chart_id
                ):
                    await handler.update(
                        visual_item.chart_id,
                        visual_data.chart_data.model_dump(),
                        repos,
                    )
                elif (
                    visual_type.name == "image"
                    and visual_data.image_data
                    and visual_item.image_id
                ):
                    await handler.update(
                        visual_item.image_id,
                        visual_data.image_data.model_dump(),
                        repos,
                    )

                await self.db.flush()
                return {
                    "id": visual_item.id,
                    "visual_type_id": visual_item.visual_type_id,
                    "paragraph_id": visual_item.paragraph_id,
                    "start_time": visual_item.start_time,
                    "table_id": visual_item.table_id,
                    "chart_id": visual_item.chart_id,
                    "image_id": visual_item.image_id,
                }
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to update visual data",
                additional_info={"error": str(e), "visual_id": str(visual_id)},
            )

    async def delete_visual_data(self, visual_id: uuid.UUID) -> bool:
        """
        Delete visual data using registry pattern.
        """
        try:
            async with self.db.begin():
                # Get the visual item first to know which specific data to delete
                visual_item = await self.visual_repo.get(visual_id)
                if not visual_item:
                    raise ServiceException(
                        status_code=404,
                        detail="Visual item not found",
                        additional_info={"visual_id": str(visual_id)},
                    )

                # Get visual type to determine handler
                visual_type = await self.visual_type_repo.get(visual_item.visual_type_id)
                if visual_type:
                    handler = self.visual_registry.get_handler(visual_type.name)
                    repos = {
                        "table_repo": self.table_repo,
                        "chart_repo": self.chart_repo,
                        "image_repo": self.image_repo,
                    }

                    # Delete the specific data first
                    if visual_item.table_id:
                        await handler.delete(visual_item.table_id, repos)
                    elif visual_item.chart_id:
                        await handler.delete(visual_item.chart_id, repos)
                    elif visual_item.image_id:
                        await handler.delete(visual_item.image_id, repos)

                # Then delete the visual item
                success = await self.visual_repo.delete(visual_id)
                if not success:
                    raise ServiceException(
                        status_code=404,
                        detail="Visual item not found",
                        additional_info={"visual_id": str(visual_id)},
                    )
                return success
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to delete visual data",
                additional_info={"error": str(e), "visual_id": str(visual_id)},
            )

    async def get_visual_data(self, visual_id: uuid.UUID) -> dict:
        """
        Get visual data by visual item ID with full details.
        """
        try:
            visual_item = await self.visual_repo.get(visual_id)
            if not visual_item:
                raise ServiceException(
                    status_code=404,
                    detail="Visual item not found",
                    additional_info={"visual_id": str(visual_id)},
                )

            # Get the specific data based on type
            specific_data = None
            if visual_item.table_id:
                specific_data = await self.table_repo.get(visual_item.table_id)
            elif visual_item.chart_id:
                specific_data = await self.chart_repo.get(visual_item.chart_id)
            elif visual_item.image_id:
                specific_data = await self.image_repo.get(visual_item.image_id)

            visual_response = {
                "id": visual_item.id,
                "visual_type_id": visual_item.visual_type_id,
                "paragraph_id": visual_item.paragraph_id,
                "start_time": visual_item.start_time,
                "table_id": visual_item.table_id,
                "chart_id": visual_item.chart_id,
                "image_id": visual_item.image_id,
                "data": specific_data.__dict__ if specific_data else None,
            }
            return visual_response
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to get visual data",
                additional_info={"error": str(e), "visual_id": str(visual_id)},
            )

    async def create_video_with_upload(
        self, video_data: InteractiveVideoUploadSchema, video_file: UploadFile
    ) -> dict:
        """
        Create a new video with file upload, store video file, and update asset file reference.
        """
        try:
            async with self.db.begin():
                # 1. Upload video file to storage
                storage_path, video_url, _ = await self.storage_service.upload_file(
                    file=video_file,
                    bucket_name=StorageBucket.INTERACTIVE_BUCKET,
                    folder_prefix=StorageBucket.VIDEO_FOLDER
                )

                # 2. Create video with uploaded URL
                video_dict = {
                    "chapter_id": video_data.chapter_id,
                    "quiz_id": video_data.quiz_id,
                    "title": video_data.title,
                    "url": video_url,  # Use uploaded video URL
                    "video_duration": video_data.video_duration,
                    "view_index": video_data.view_index,
                }
                video = await self.video_repo.create(video_dict)
                await self.db.flush()

                # 3. Update asset file with video_id
                if video_data.asset_file_id:
                    asset_file = await self.file_repo.get(video_data.asset_file_id)
                    if not asset_file:
                        raise ServiceException(
                            status_code=404,
                            detail="Asset file not found",
                            additional_info={"asset_file_id": str(video_data.asset_file_id)},
                        )

                    await self.file_repo.update(video_data.asset_file_id, {"video_id": video.id})

                # 4. Create keyword type styles for this video
                if video_data.keyword_styles:
                    # Create provided keyword styles
                    for style_data in video_data.keyword_styles:
                        style_dict = {
                            "video_id": video.id,
                            "keyword_type_id": style_data.keyword_type_id,
                            "color_light": style_data.color_light,
                            "color_dark": style_data.color_dark,
                            "shadow_light": style_data.shadow_light,
                            "shadow_dark": style_data.shadow_dark,
                            "size": style_data.size,
                        }
                        await self.keyword_style_repo.create(style_dict)
                else:
                    # Create default keyword type styles for all available keyword types
                    all_keyword_types = await self.keyword_type_repo.get_all(page=1, limit=100)
                    for keyword_type in all_keyword_types:
                        style_dict = {
                            "video_id": video.id,
                            "keyword_type_id": keyword_type.id,
                            "color_light": "#000000",
                            "color_dark": "#FFFFFF", 
                            "shadow_light": None,
                            "shadow_dark": None,
                            "size": 14,
                        }
                        await self.keyword_style_repo.create(style_dict)

                # 5. Create paragraphs data (same as regular create_video)
                for paragraph_data in video_data.paragraphs:
                    paragraph_dict = {
                        "video_id": video.id,
                        "paragraph_text": paragraph_data.paragraph_text,
                        "start_time": paragraph_data.start_time,
                        "end_time": paragraph_data.end_time,
                        "view_index": paragraph_data.view_index,
                    }
                    paragraph = await self.paragraph_repo.create(paragraph_dict)
                    await self.db.flush()

                    # Create words for this paragraph
                    for word_data in paragraph_data.words:
                        word_dict = {
                            "paragraph_id": paragraph.id,
                            "type_id": word_data.word_type_id,
                            "word": word_data.word,
                            "start_time": word_data.start_time,
                            "end_time": word_data.end_time,
                        }
                        await self.word_repo.create(word_dict)

                    # Create keywords for this paragraph
                    for keyword_data in paragraph_data.keywords:
                        keyword_dict = {
                            "paragraph_id": paragraph.id,
                            "type_id": keyword_data.keyword_type_id,
                            "word": keyword_data.word,
                        }
                        await self.keyword_repo.create(keyword_dict)

                    # Create visual data if provided
                    if paragraph_data.visual_data:
                        await self._create_visual_data_with_registry(
                            paragraph.id, paragraph_data.visual_data
                        )

                await self.db.flush()

                return await self.video_repo.get_video_with_paragraphs(
                    video_id=video.id
                    )

        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create video with upload",
                additional_info={
                    "error": str(e),
                    "video_data": str(video_data),
                    "filename": video_file.filename,
                },
            )

    async def update_video_keyword_styles(
        self, video_id: UUID, keyword_styles: List[VideoKeywordStyleUpdateSchema]
    ) -> dict:
        """
        Update keyword styles for a specific video.
        """
        try:
            async with self.db.begin():
                # 1. Verify video exists
                video = await self.video_repo.get(video_id)
                if not video:
                    raise ServiceException(
                        status_code=404,
                        detail="Video not found",
                        additional_info={"video_id": str(video_id)},
                    )

                updated_styles = []

                # 2. Update each keyword style
                for style_update in keyword_styles:
                    # Find existing style for this video and keyword type
                    existing_styles = await self.keyword_style_repo.get_all(page=1, limit=1000)
                    existing_style = None

                    for style in existing_styles:
                        if (style.video_id == video_id and 
                            style.keyword_type_id == style_update.keyword_type_id):
                            existing_style = style
                            break

                    if existing_style:
                        # Update existing style
                        update_data = {}
                        if style_update.color_light is not None:
                            update_data["color_light"] = style_update.color_light
                        if style_update.color_dark is not None:
                            update_data["color_dark"] = style_update.color_dark
                        if style_update.shadow_light is not None:
                            update_data["shadow_light"] = style_update.shadow_light
                        if style_update.shadow_dark is not None:
                            update_data["shadow_dark"] = style_update.shadow_dark
                        if style_update.size is not None:
                            update_data["size"] = style_update.size

                        if update_data:
                            updated_style = await self.keyword_style_repo.update(
                                existing_style.id, update_data
                            )
                            updated_styles.append(updated_style)
                    else:
                        # Create new style if it doesn't exist
                        create_data = {
                            "video_id": video_id,
                            "keyword_type_id": style_update.keyword_type_id,
                            "color_light": style_update.color_light or "#000000",
                            "color_dark": style_update.color_dark or "#FFFFFF",
                            "shadow_light": style_update.shadow_light,
                            "shadow_dark": style_update.shadow_dark,
                            "size": style_update.size or 14,
                        }
                        new_style = await self.keyword_style_repo.create(create_data)
                        updated_styles.append(new_style)

                await self.db.flush()
                return {
                    "video_id": video_id,
                    "updated_styles_count": len(updated_styles),
                    "updated_styles": [
                        {
                            "keyword_type_id": str(style.keyword_type_id),
                            "color_light": style.color_light,
                            "color_dark": style.color_dark,
                            "shadow_light": style.shadow_light,
                            "shadow_dark": style.shadow_dark,
                            "size": style.size,
                        }
                        for style in updated_styles
                    ],
                }

        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to update video keyword styles",
                additional_info={
                    "error": str(e),
                    "video_id": str(video_id),
                    "keyword_styles_count": len(keyword_styles),
                },
            )

    async def _link_assist_image_to_visual_item(
        self, assist_image_id: uuid.UUID, visual_item_id: uuid.UUID
    ) -> None:
        """Helper method to link an assist image to a visual item."""
        try:
            from app.models.interactive_models.assist_image_model import AssistImageModel
            from sqlalchemy import update

            # Update the assist image to link to the visual item
            stmt = (
                update(AssistImageModel)
                .where(AssistImageModel.id == assist_image_id)
                .values(visual_item_id=visual_item_id)
            )
            await self.db.execute(stmt)

        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to link assist image to visual item",
                additional_info={
                    "error": str(e),
                    "assist_image_id": str(assist_image_id),
                    "visual_item_id": str(visual_item_id),
                },
            )
