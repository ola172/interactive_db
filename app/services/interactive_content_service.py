import uuid
from typing import Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exception import CustomException
from app.exceptions.service_exception import ServiceException
from app.helper import VisualDataRegistry
from app.repositories.interactive_repositories import (
    InteractiveParagraphRepository,
    WordTypeRepository,
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
from app.schemas.interactive_schemas import (
    InteractiveKeywordCreateSchema,
    InteractiveKeywordUpdateSchema,
    KeyWordTypeCreateSchema,
    KeyWordTypeUpdateSchema,
    WordTypeCreateSchema,
    WordTypeUpdateSchema,
    VisualTypeCreateSchema,
    VisualTypeUpdateSchema,
    ChartTypeCreateSchema,
    ChartTypeUpdateSchema,
    VisualDataCreateSchema,
    VisualDataUpdateSchema,
)

class InteractiveContentService:
    def __init__(
        self,
        db: AsyncSession,
        paragraph_repo: InteractiveParagraphRepository,
        word_type_repo: WordTypeRepository,
        keyword_repo: InteractiveKeyWordRepository,
        keyword_type_repo: KeyWordTypeRepository,
        video_keyword_style_repo: VideoKeywordTypeStyleRepository,
        visual_repo: VisualItemRepository,
        visual_type_repo: VisualTypeRepository,
        table_repo: TableDataRepository,
        chart_repo: ChartDataRepository,
        chart_type_repo: ChartTypeRepository,
        image_repo: ImageRepository,
    ):
        self.db = db
        self.paragraph_repo = paragraph_repo
        self.word_type_repo = word_type_repo
        self.keyword_repo = keyword_repo
        self.keyword_type_repo = keyword_type_repo
        self.video_keyword_style_repo = video_keyword_style_repo
        self.visual_repo = visual_repo
        self.visual_type_repo = visual_type_repo
        self.table_repo = table_repo
        self.chart_repo = chart_repo
        self.chart_type_repo = chart_type_repo
        self.image_repo = image_repo

        # Initialize visual data registry
        self.visual_registry = VisualDataRegistry()

    async def get_paragraphs_by_video(self, video_id: uuid.UUID) -> list[dict]:
        """Get all paragraphs for a specific video with interactive content."""
        try:
            paragraphs = await self.paragraph_repo.get_paragraphs_by_video_id(video_id)
            return paragraphs
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to get paragraphs by video",
                additional_info={"error": str(e), "video_id": str(video_id)},
            )

    async def get_paragraph_with_details(self, paragraph_id: uuid.UUID) -> dict:
        """Get a paragraph with all its interactive details (words, keywords, visuals)."""
        try:
            paragraph = await self.paragraph_repo.get_paragraph_with_details(
                paragraph_id
            )
            if not paragraph:
                raise ServiceException(
                    status_code=404,
                    detail="Paragraph not found",
                    additional_info={"paragraph_id": str(paragraph_id)},
                )
            return paragraph
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to get paragraph details",
                additional_info={"error": str(e), "paragraph_id": str(paragraph_id)},
            )

    async def create_keyword(
        self, paragraph_id: uuid.UUID, keyword_data: InteractiveKeywordCreateSchema
    ) -> dict:
        """Create a new interactive keyword for a specific paragraph."""
        try:
            async with self.db.begin():
                # Add paragraph_id to the keyword data and map keyword_type_id to type_id
                keyword_dict = keyword_data.model_dump()
                keyword_dict["paragraph_id"] = paragraph_id
                keyword_dict["type_id"] = keyword_dict.pop(
                    "keyword_type_id"
                )  # Remove keyword_type_id and use type_id

                keyword = await self.keyword_repo.create(keyword_dict)
                return {
                    "id": keyword.id,
                    "paragraph_id": keyword.paragraph_id,
                    "type_id": keyword.type_id,
                    "word": keyword.word,
                }
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create keyword",
                additional_info={
                    "error": str(e),
                    "paragraph_id": str(paragraph_id),
                    "data": keyword_data.model_dump(),
                },
            )

    async def get_keywords_by_paragraph(self, paragraph_id: uuid.UUID) -> list[dict]:
        """Get all keywords for a specific paragraph."""
        try:
            keywords = await self.keyword_repo.get_keywords_by_paragraph_id(
                paragraph_id
            )
            return keywords
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to get keywords by paragraph",
                additional_info={"error": str(e), "paragraph_id": str(paragraph_id)},
            )

    async def update_keyword(
        self, keyword_id: uuid.UUID, keyword_update: InteractiveKeywordUpdateSchema
    ) -> dict:
        """Update keyword (name, type, style)."""
        try:
            async with self.db.begin():
                update_data = {}
                if keyword_update.word is not None:
                    update_data["word"] = keyword_update.word
                if keyword_update.keyword_type_id is not None:
                    update_data["type_id"] = keyword_update.keyword_type_id

                if not update_data:
                    raise ServiceException(
                        status_code=400,
                        detail="No fields to update",
                        additional_info={"keyword_id": str(keyword_id)},
                    )

                keyword = await self.keyword_repo.update(keyword_id, update_data)
                if not keyword:
                    raise ServiceException(
                        status_code=404,
                        detail="Keyword not found",
                        additional_info={"keyword_id": str(keyword_id)},
                    )

                return {
                    "id": keyword.id,
                    "paragraph_id": keyword.paragraph_id,
                    "type_id": keyword.type_id,
                    "word": keyword.word,
                }
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to update keyword",
                additional_info={"error": str(e), "keyword_id": str(keyword_id)},
            )

    async def delete_keyword(self, keyword_id: uuid.UUID) -> bool:
        """Delete a keyword item."""
        try:
            async with self.db.begin():
                success = await self.keyword_repo.delete(keyword_id)
                if not success:
                    raise ServiceException(
                        status_code=404,
                        detail="Keyword not found",
                        additional_info={"keyword_id": str(keyword_id)},
                    )
                return success
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to delete keyword",
                additional_info={"error": str(e), "keyword_id": str(keyword_id)},
            )

    async def get_visual_by_paragraph(self, paragraph_id: uuid.UUID) -> Optional[dict]:
        """Get the visual item for a specific paragraph."""
        try:
            visual = await self.visual_repo.get_visual_by_paragraph_id(paragraph_id)
            return visual
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to get visual by paragraph",
                additional_info={"error": str(e), "paragraph_id": str(paragraph_id)},
            )

    async def create_visual_data(
        self, paragraph_id: uuid.UUID, visual_data: VisualDataCreateSchema
    ) -> dict:
        """Create visual data using registry pattern to determine handler based on visual_type_id."""
        try:
            async with self.db.begin():
                # Get visual type by ID
                visual_type = await self.visual_type_repo.get(
                    visual_data.visual_type_id
                )
                if not visual_type:
                    raise ServiceException(
                        status_code=400,
                        detail="Visual type not found",
                        additional_info={
                            "visual_type_id": str(visual_data.visual_type_id)
                        },
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
                    "table_id": (
                        specific_data_id if visual_type.name == "table" else None
                    ),
                    "chart_id": (
                        specific_data_id if visual_type.name == "chart" else None
                    ),
                    "image_id": (
                        specific_data_id if visual_type.name == "image" else None
                    ),
                }
                visual_item = await self.visual_repo.create(visual_dict)

                # Link assist image if provided
                if visual_data.assist_image_id:
                    await self._link_assist_image_to_visual_item(
                        visual_data.assist_image_id, visual_item.id
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
                    "assist_image_id": getattr(visual_item, 'assist_image_id', None) if hasattr(visual_item, 'assist_image') and visual_item.assist_image else None,
                }
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create visual data",
                additional_info={"error": str(e), "paragraph_id": str(paragraph_id)},
            )

    async def update_visual_data(
        self, visual_id: uuid.UUID, visual_update: VisualDataUpdateSchema
    ) -> dict:
        """Update visual data using registry pattern."""
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
                if visual_update.visual_type_id is not None:
                    visual_update_data["visual_type_id"] = visual_update.visual_type_id
                if visual_update.start_time is not None:
                    visual_update_data["start_time"] = visual_update.start_time

                if visual_update_data:
                    visual_item = await self.visual_repo.update(
                        visual_id, visual_update_data
                    )

                # Get visual type to determine handler
                visual_type = await self.visual_type_repo.get(
                    visual_item.visual_type_id
                )
                if not visual_type:
                    raise ServiceException(
                        status_code=400,
                        detail="Visual type not found",
                        additional_info={
                            "visual_type_id": str(visual_item.visual_type_id)
                        },
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
                    and visual_update.table_data
                    and visual_item.table_id
                ):
                    await handler.update(
                        visual_item.table_id,
                        visual_update.table_data.model_dump(),
                        repos,
                    )
                elif (
                    visual_type.name == "chart"
                    and visual_update.chart_data
                    and visual_item.chart_id
                ):
                    await handler.update(
                        visual_item.chart_id,
                        visual_update.chart_data.model_dump(),
                        repos,
                    )
                elif (
                    visual_type.name == "image"
                    and visual_update.image_data
                    and visual_item.image_id
                ):
                    await handler.update(
                        visual_item.image_id,
                        visual_update.image_data.model_dump(),
                        repos,
                    )

                # Handle assist image linking/unlinking
                if visual_update.assist_image_id is not None:
                    # First, unlink any existing assist image
                    if hasattr(visual_item, 'assist_image') and visual_item.assist_image:
                        await self.unlink_assist_image_from_visual_item(
                            visual_item.assist_image.id
                        )
                    
                    # Link new assist image if provided
                    if visual_update.assist_image_id:
                        await self._link_assist_image_to_visual_item(
                            visual_update.assist_image_id, visual_item.id
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
                    "assist_image_id": getattr(visual_item, 'assist_image_id', None) if hasattr(visual_item, 'assist_image') and visual_item.assist_image else None,
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
        """Delete visual data using registry pattern."""
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
                visual_type = await self.visual_type_repo.get(
                    visual_item.visual_type_id
                )
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

    async def get_video_keyword_styles(self, video_id: uuid.UUID) -> list[dict]:
        """Get all keyword styles for a specific video."""
        try:
            styles = await self.video_keyword_style_repo.get_styles_by_video_id(
                video_id
            )
            return [
                {
                    "id": style.id,
                    "video_id": style.video_id,
                    "keyword_type_id": style.keyword_type_id,
                    "keyword_type_name": style.type.name if style.type else None,
                    "color_light": style.color_light,
                    "color_dark": style.color_dark,
                    "shadow_light": style.shadow_light,
                    "shadow_dark": style.shadow_dark,
                    "size": style.size,
                }
                for style in styles
            ]
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to get video keyword styles",
                additional_info={"error": str(e), "video_id": str(video_id)},
            )

    # Keyword Type CRUD operations
    async def create_keyword_type(
        self, keyword_type_data: KeyWordTypeCreateSchema
    ) -> dict:
        """Create a new keyword type."""
        try:
            async with self.db.begin():
                keyword_type = await self.keyword_type_repo.create(
                    keyword_type_data.model_dump()
                )
                return {
                    "id": keyword_type.id,
                    "name": keyword_type.name,
                    "description": keyword_type.description,
                }
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create keyword type",
                additional_info={
                    "error": str(e),
                    "data": keyword_type_data.model_dump(),
                },
            )

    async def get_all_keyword_types(self) -> list[dict]:
        """Get all available keyword types."""
        try:
            keyword_types = await self.keyword_type_repo.get_all(page=1, limit=1000)
            return [
                {
                    "id": ktype.id,
                    "name": ktype.name,
                    "description": getattr(ktype, "description", None),
                }
                for ktype in keyword_types
            ]
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to get keyword types",
                additional_info={"error": str(e)},
            )

    async def update_keyword_type(
        self, keyword_type_id: uuid.UUID, keyword_type_update: KeyWordTypeUpdateSchema
    ) -> dict:
        """Update a keyword type."""
        try:
            async with self.db.begin():
                update_data = {}
                if keyword_type_update.name is not None:
                    update_data["name"] = keyword_type_update.name
                if keyword_type_update.description is not None:
                    update_data["description"] = keyword_type_update.description

                if not update_data:
                    raise ServiceException(
                        status_code=400,
                        detail="No fields to update",
                        additional_info={"keyword_type_id": str(keyword_type_id)},
                    )

                keyword_type = await self.keyword_type_repo.update(
                    keyword_type_id, update_data
                )
                if not keyword_type:
                    raise ServiceException(
                        status_code=404,
                        detail="Keyword type not found",
                        additional_info={"keyword_type_id": str(keyword_type_id)},
                    )

                return {
                    "id": keyword_type.id,
                    "name": keyword_type.name,
                    "description": getattr(keyword_type, "description", None),
                }
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to update keyword type",
                additional_info={
                    "error": str(e),
                    "keyword_type_id": str(keyword_type_id),
                },
            )

    async def delete_keyword_type(self, keyword_type_id: uuid.UUID) -> bool:
        """Delete a keyword type."""
        try:
            async with self.db.begin():
                success = await self.keyword_type_repo.delete(keyword_type_id)
                if not success:
                    raise ServiceException(
                        status_code=404,
                        detail="Keyword type not found",
                        additional_info={"keyword_type_id": str(keyword_type_id)},
                    )
                return success
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to delete keyword type",
                additional_info={
                    "error": str(e),
                    "keyword_type_id": str(keyword_type_id),
                },
            )

    # Word Type CRUD operations
    async def create_word_type(self, word_type_data: WordTypeCreateSchema) -> dict:
        """Create a new word type."""
        try:
            async with self.db.begin():
                word_type = await self.word_type_repo.create(
                    word_type_data.model_dump()
                )
                return {
                    "id": word_type.id,
                    "name": word_type.name,
                    "description": word_type.description,
                }
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create word type",
                additional_info={"error": str(e), "data": word_type_data.model_dump()},
            )

    async def get_all_word_types(self) -> list[dict]:
        """Get all available word types."""
        try:
            word_types = await self.word_type_repo.get_all(page=1, limit=1000)
            return [
                {
                    "id": wtype.id,
                    "name": wtype.name,
                    "description": getattr(wtype, "description", None),
                }
                for wtype in word_types
            ]
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to get word types",
                additional_info={"error": str(e)},
            )

    async def update_word_type(
        self, word_type_id: uuid.UUID, word_type_update: WordTypeUpdateSchema
    ) -> dict:
        """Update a word type."""
        try:
            async with self.db.begin():
                update_data = {}
                if word_type_update.name is not None:
                    update_data["name"] = word_type_update.name
                if word_type_update.description is not None:
                    update_data["description"] = word_type_update.description

                if not update_data:
                    raise ServiceException(
                        status_code=400,
                        detail="No fields to update",
                        additional_info={"word_type_id": str(word_type_id)},
                    )

                word_type = await self.word_type_repo.update(word_type_id, update_data)
                if not word_type:
                    raise ServiceException(
                        status_code=404,
                        detail="Word type not found",
                        additional_info={"word_type_id": str(word_type_id)},
                    )

                return {
                    "id": word_type.id,
                    "name": word_type.name,
                    "description": getattr(word_type, "description", None),
                }
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to update word type",
                additional_info={"error": str(e), "word_type_id": str(word_type_id)},
            )

    async def delete_word_type(self, word_type_id: uuid.UUID) -> bool:
        """Delete a word type."""
        try:
            async with self.db.begin():
                success = await self.word_type_repo.delete(word_type_id)
                if not success:
                    raise ServiceException(
                        status_code=404,
                        detail="Word type not found",
                        additional_info={"word_type_id": str(word_type_id)},
                    )
                return success
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to delete word type",
                additional_info={"error": str(e), "word_type_id": str(word_type_id)},
            )

    # Visual Type CRUD operations
    async def create_visual_type(
        self, visual_type_data: VisualTypeCreateSchema
    ) -> dict:
        """Create a new visual type."""
        try:
            async with self.db.begin():
                visual_type = await self.visual_type_repo.create(
                    visual_type_data.model_dump()
                )
                return {
                    "id": visual_type.id,
                    "name": visual_type.name,
                    "description": visual_type.description,
                }
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create visual type",
                additional_info={
                    "error": str(e),
                    "data": visual_type_data.model_dump(),
                },
            )

    async def get_all_visual_types(self) -> list[dict]:
        """Get all available visual types."""
        try:
            visual_types = await self.visual_type_repo.get_all(page=1, limit=1000)
            return [
                {
                    "id": vtype.id,
                    "name": vtype.name,
                    "description": getattr(vtype, "description", None),
                }
                for vtype in visual_types
            ]
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to get visual types",
                additional_info={"error": str(e)},
            )

    async def update_visual_type(
        self, visual_type_id: uuid.UUID, visual_type_update: VisualTypeUpdateSchema
    ) -> dict:
        """Update a visual type."""
        try:
            async with self.db.begin():
                update_data = {}
                if visual_type_update.name is not None:
                    update_data["name"] = visual_type_update.name
                if visual_type_update.description is not None:
                    update_data["description"] = visual_type_update.description

                if not update_data:
                    raise ServiceException(
                        status_code=400,
                        detail="No fields to update",
                        additional_info={"visual_type_id": str(visual_type_id)},
                    )

                visual_type = await self.visual_type_repo.update(
                    visual_type_id, update_data
                )
                if not visual_type:
                    raise ServiceException(
                        status_code=404,
                        detail="Visual type not found",
                        additional_info={"visual_type_id": str(visual_type_id)},
                    )

                return {
                    "id": visual_type.id,
                    "name": visual_type.name,
                    "description": getattr(visual_type, "description", None),
                }
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to update visual type",
                additional_info={
                    "error": str(e),
                    "visual_type_id": str(visual_type_id),
                },
            )

    async def delete_visual_type(self, visual_type_id: uuid.UUID) -> bool:
        """Delete a visual type."""
        try:
            async with self.db.begin():
                success = await self.visual_type_repo.delete(visual_type_id)
                if not success:
                    raise ServiceException(
                        status_code=404,
                        detail="Visual type not found",
                        additional_info={"visual_type_id": str(visual_type_id)},
                    )
                return success
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to delete visual type",
                additional_info={
                    "error": str(e),
                    "visual_type_id": str(visual_type_id),
                },
            )

    # Chart Type CRUD operations
    async def create_chart_type(self, chart_type_data: ChartTypeCreateSchema) -> dict:
        """Create a new chart type."""
        try:
            async with self.db.begin():
                chart_type = await self.chart_type_repo.create(
                    chart_type_data.model_dump()
                )
                return {
                    "id": chart_type.id,
                    "name": chart_type.name,
                    "description": chart_type.description,
                }
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create chart type",
                additional_info={"error": str(e), "data": chart_type_data.model_dump()},
            )

    async def get_all_chart_types(self) -> list[dict]:
        """Get all available chart types."""
        try:
            chart_types = await self.chart_type_repo.get_all(page=1, limit=1000)
            return [
                {
                    "id": ctype.id,
                    "name": ctype.name,
                    "description": getattr(ctype, "description", None),
                }
                for ctype in chart_types
            ]
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to get chart types",
                additional_info={"error": str(e)},
            )

    async def update_chart_type(
        self, chart_type_id: uuid.UUID, chart_type_update: ChartTypeUpdateSchema
    ) -> dict:
        """Update a chart type."""
        try:
            async with self.db.begin():
                update_data = {}
                if chart_type_update.name is not None:
                    update_data["name"] = chart_type_update.name
                if chart_type_update.description is not None:
                    update_data["description"] = chart_type_update.description

                if not update_data:
                    raise ServiceException(
                        status_code=400,
                        detail="No fields to update",
                        additional_info={"chart_type_id": str(chart_type_id)},
                    )

                chart_type = await self.chart_type_repo.update(
                    chart_type_id, update_data
                )
                if not chart_type:
                    raise ServiceException(
                        status_code=404,
                        detail="Chart type not found",
                        additional_info={"chart_type_id": str(chart_type_id)},
                    )

                return {
                    "id": chart_type.id,
                    "name": chart_type.name,
                    "description": getattr(chart_type, "description", None),
                }
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to update chart type",
                additional_info={"error": str(e), "chart_type_id": str(chart_type_id)},
            )

    async def delete_chart_type(self, chart_type_id: uuid.UUID) -> bool:
        """Delete a chart type."""
        try:
            async with self.db.begin():
                success = await self.chart_type_repo.delete(chart_type_id)
                if not success:
                    raise ServiceException(
                        status_code=404,
                        detail="Chart type not found",
                        additional_info={"chart_type_id": str(chart_type_id)},
                    )
                return success
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to delete chart type",
                additional_info={"error": str(e), "chart_type_id": str(chart_type_id)},
            )

    # Visual Data Retrieval Methods
    async def get_visual_data_by_id(self, visual_id: uuid.UUID) -> dict:
        """Get visual data by visual_id with full content."""
        try:
            visual_item = await self.visual_repo.get(visual_id)
            if not visual_item:
                raise ServiceException(
                    status_code=404,
                    detail="Visual item not found",
                    additional_info={"visual_id": str(visual_id)},
                )

            # Get visual type to determine what data to fetch
            visual_type = await self.visual_type_repo.get(visual_item.visual_type_id)
            if not visual_type:
                raise ServiceException(
                    status_code=500,
                    detail="Visual type not found",
                    additional_info={"visual_type_id": str(visual_item.visual_type_id)},
                )

            # Fetch the specific data based on visual type
            specific_data = None
            if visual_type.name == "table" and visual_item.table_id:
                specific_data = await self.table_repo.get(visual_item.table_id)
            elif visual_type.name == "chart" and visual_item.chart_id:
                chart_data = await self.chart_repo.get(visual_item.chart_id)
                if chart_data:
                    chart_type = await self.chart_type_repo.get(
                        chart_data.chart_type_id
                    )
                    specific_data = {
                        "id": chart_data.id,
                        "chart_type_id": chart_data.chart_type_id,
                        "chart_type_name": chart_type.name if chart_type else None,
                        "labels": chart_data.labels,
                        "data": chart_data.data,
                        "title": chart_data.title,
                    }
            elif visual_type.name == "image" and visual_item.image_id:
                specific_data = await self.image_repo.get(visual_item.image_id)

            return {
                "id": visual_item.id,
                "visual_type_id": visual_item.visual_type_id,
                "visual_type_name": visual_type.name,
                "paragraph_id": visual_item.paragraph_id,
                "start_time": visual_item.start_time,
                "table_id": visual_item.table_id,
                "chart_id": visual_item.chart_id,
                "image_id": visual_item.image_id,
                "assist_image_id": visual_item.assist_image_id,
                "data": (
                    specific_data.__dict__
                    if hasattr(specific_data, "__dict__")
                    and not isinstance(specific_data, dict)
                    else specific_data
                ),
            }
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to get visual data by id",
                additional_info={"error": str(e), "visual_id": str(visual_id)},
            )

    async def get_visual_data_by_type_id(self, visual_type_id: uuid.UUID) -> list[dict]:
        """Get all visual data items by visual_type_id."""
        try:
            # Get visual type first
            visual_type = await self.visual_type_repo.get(visual_type_id)
            if not visual_type:
                raise ServiceException(
                    status_code=404,
                    detail="Visual type not found",
                    additional_info={"visual_type_id": str(visual_type_id)},
                )

            # Get all visual items for this type
            visual_items = await self.visual_repo.get_visuals_by_type(visual_type.name)

            result = []
            for visual_item in visual_items:
                # Fetch the specific data for each visual item
                specific_data = None
                if visual_type.name == "table" and visual_item.table_id:
                    specific_data = await self.table_repo.get(visual_item.table_id)
                elif visual_type.name == "chart" and visual_item.chart_id:
                    chart_data = await self.chart_repo.get(visual_item.chart_id)
                    if chart_data:
                        chart_type = await self.chart_type_repo.get(
                            chart_data.chart_type_id
                        )
                        specific_data = {
                            "id": chart_data.id,
                            "chart_type_id": chart_data.chart_type_id,
                            "chart_type_name": chart_type.name if chart_type else None,
                            "labels": chart_data.labels,
                            "data": chart_data.data,
                            "title": chart_data.title,
                        }
                elif visual_type.name == "image" and visual_item.image_id:
                    specific_data = await self.image_repo.get(visual_item.image_id)

                result.append(
                    {
                        "id": visual_item.id,
                        "visual_type_id": visual_item.visual_type_id,
                        "visual_type_name": visual_type.name,
                        "paragraph_id": visual_item.paragraph_id,
                        "start_time": visual_item.start_time,
                        "table_id": visual_item.table_id,
                        "chart_id": visual_item.chart_id,
                        "image_id": visual_item.image_id,
                        "assist_image_id": visual_item.assist_image_id,
                        "data": (
                            specific_data.__dict__
                            if hasattr(specific_data, "__dict__")
                            and not isinstance(specific_data, dict)
                            else specific_data
                        ),
                    }
                )

            return result
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to get visual data by type id",
                additional_info={
                    "error": str(e),
                    "visual_type_id": str(visual_type_id),
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

    async def unlink_assist_image_from_visual_item(
        self, assist_image_id: uuid.UUID
    ) -> bool:
        """Unlink an assist image from its visual item (set visual_item_id to None)."""
        try:
            from app.models.interactive_models.assist_image_model import AssistImageModel
            from sqlalchemy import update

            stmt = (
                update(AssistImageModel)
                .where(AssistImageModel.id == assist_image_id)
                .values(visual_item_id=None)
            )
            result = await self.db.execute(stmt)
            return result.rowcount > 0

        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to unlink assist image from visual item",
                additional_info={
                    "error": str(e),
                    "assist_image_id": str(assist_image_id),
                },
            )

    async def get_orphaned_assist_images(self) -> list[dict]:
        """Get assist images that are not linked to any visual item."""
        try:
            from app.models.interactive_models.assist_image_model import AssistImageModel
            from sqlalchemy import select

            stmt = select(AssistImageModel).where(
                AssistImageModel.visual_item_id.is_(None)
            )
            result = await self.db.execute(stmt)
            orphaned_images = result.scalars().all()

            return [
                {
                    "id": img.id,
                    "image_title": img.image_title,
                    "description": img.description,
                    "created_at": img.created_at,
                    "file_id": img.file_id,
                }
                for img in orphaned_images
            ]

        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to get orphaned assist images",
                additional_info={"error": str(e)},
            )
