import uuid
from fastapi import APIRouter, Depends, HTTPException

from app.container import get_db_session
from app.exceptions.custom_exception import CustomHTTPException, CustomException
from app.schemas.interactive_schemas import (
    InteractiveParagraphCreateSchema,
    InteractiveWordCreateSchema,
    InteractiveKeyWordCreateSchema,
    VideoKeywordTypeStyleCreateSchema,
    VisualItemCreateSchema,
    TableDataCreateSchema,
    ChartDataCreateSchema,
    ImageCreateSchema,
    WordTypeCreateSchema,
    KeyWordTypeCreateSchema,
    VisualTypeCreateSchema,
    ChartTypeCreateSchema,
)
from app.schemas.interactive_schemas import (
    InteractiveKeywordUpdateSchema,
    VisualDataUpdateSchema,
)
from app.repositories.interactive_repositories import (
    InteractiveParagraphRepository,
    InteractiveWordRepository,
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
from sqlalchemy.ext.asyncio import AsyncSession

interactive_content_router = APIRouter(prefix="/interactive-content", tags=["Interactive Content"])


# Paragraph routes

@interactive_content_router.get("/videos/{video_id}/paragraphs")
async def get_paragraphs_by_video(
    video_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get all paragraphs for a specific video with interactive content.
    """
    try:
        paragraph_repo = InteractiveParagraphRepository(db)
        paragraphs = await paragraph_repo.get_paragraphs_by_video_id(video_id)
        return {"results": paragraphs}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )


# @interactive_content_router.post("/paragraphs")
# async def create_paragraph(
#     paragraph_data: InteractiveParagraphCreateSchema,
#     db: AsyncSession = Depends(get_db_session)
# ):
#     """
#     Create a new interactive paragraph.
#     """
#     try:
#         paragraph_repo = InteractiveParagraphRepository(db)
#         paragraph = await paragraph_repo.create(paragraph_data.model_dump())
#         return {"results": paragraph}
#     except CustomException as e:
#         raise CustomHTTPException(
#             status_code=e.status_code,
#             detail=e.detail,
#             exception_type=e.exception_type,
#             additional_info=e.additional_info,
#         )
#     except Exception as e:
#         raise CustomHTTPException(
#             status_code=500,
#             detail="Internal server error",
#             exception_type="InternalServerError",
#             additional_info={"error": str(e)},
#         )


@interactive_content_router.get("/paragraphs/{paragraph_id}/details")
async def get_paragraph_with_details(
    paragraph_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get a paragraph with all its interactive details (words, keywords, visuals).
    """
    try:
        paragraph_repo = InteractiveParagraphRepository(db)
        paragraph = await paragraph_repo.get_paragraph_with_details(paragraph_id)
        if not paragraph:
            raise HTTPException(status_code=404, detail="Paragraph not found")
        return {"results": paragraph}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )


# Word routes

# @interactive_content_router.post("/words")
# async def create_word(
#     word_data: InteractiveWordCreateSchema,
#     db: AsyncSession = Depends(get_db_session)
# ):
#     """
#     Create a new interactive word.
#     """
#     try:
#         word_repo = InteractiveWordRepository(db)
#         word = await word_repo.create(word_data.model_dump())
#         return {"results": word}
#     except CustomException as e:
#         raise CustomHTTPException(
#             status_code=e.status_code,
#             detail=e.detail,
#             exception_type=e.exception_type,
#             additional_info=e.additional_info,
#         )
#     except Exception as e:
#         raise CustomHTTPException(
#             status_code=500,
#             detail="Internal server error",
#             exception_type="InternalServerError",
#             additional_info={"error": str(e)},
#         )


# @interactive_content_router.get("/paragraphs/{paragraph_id}/words")
# async def get_words_by_paragraph(
#     paragraph_id: uuid.UUID,
#     db: AsyncSession = Depends(get_db_session)
# ):
#     """
#     Get all words for a specific paragraph.
#     """
#     try:
#         word_repo = InteractiveWordRepository(db)
#         words = await word_repo.get_words_by_paragraph_id(paragraph_id)
#         return {"results": words}
#     except CustomException as e:
#         raise CustomHTTPException(
#             status_code=e.status_code,
#             detail=e.detail,
#             exception_type=e.exception_type,
#             additional_info=e.additional_info,
#         )
#     except Exception as e:
#         raise CustomHTTPException(
#             status_code=500,
#             detail="Internal server error",
#             exception_type="InternalServerError",
#             additional_info={"error": str(e)},
#         )


# Keyword routes

@interactive_content_router.post("/keyword-types")
async def create_keyword_type(
    keyword_type_data: KeyWordTypeCreateSchema,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Create a new keyword type.
    """
    try:
        keyword_type_repo = KeyWordTypeRepository(db)
        async with db.begin():
            keyword_type = await keyword_type_repo.create(keyword_type_data.model_dump())
        return {"results": keyword_type}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )


@interactive_content_router.post("/video-keyword-styles")
async def create_video_keyword_style(
    style_data: VideoKeywordTypeStyleCreateSchema,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Create a new video keyword type style.
    """
    try:
        style_repo = VideoKeywordTypeStyleRepository(db)
        style = await style_repo.create(style_data.model_dump())
        return {"results": style}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )


@interactive_content_router.post("/keywords")
async def create_keyword(
    keyword_data: InteractiveKeyWordCreateSchema,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Create a new interactive keyword.
    """
    try:
        keyword_repo = InteractiveKeyWordRepository(db)
        keyword = await keyword_repo.create(keyword_data.model_dump())
        return {"results": keyword}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )


@interactive_content_router.get("/paragraphs/{paragraph_id}/keywords")
async def get_keywords_by_paragraph(
    paragraph_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get all keywords for a specific paragraph.
    """
    try:
        keyword_repo = InteractiveKeyWordRepository(db)
        keywords = await keyword_repo.get_keywords_by_paragraph_id(paragraph_id)
        return {"results": keywords}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )

@interactive_content_router.put("/keywords/{keyword_id}")
async def update_keyword(
    keyword_id: uuid.UUID,
    keyword_update: InteractiveKeywordUpdateSchema,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Update keyword (name, type, style).
    """
    try:
        keyword_repo = InteractiveKeyWordRepository(db)
        
        update_data = {}
        if keyword_update.word is not None:
            update_data["word"] = keyword_update.word
        if keyword_update.type_id is not None:
            update_data["type_id"] = keyword_update.type_id
            
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
            
        keyword = await keyword_repo.update(keyword_id, update_data)
        if not keyword:
            raise HTTPException(status_code=404, detail="Keyword not found")
            
        return {"results": keyword}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )
    
@interactive_content_router.delete("/keywords/{keyword_id}")
async def delete_keyword(
    keyword_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Delete a keyword item.
    """
    try:
        keyword_repo = InteractiveKeyWordRepository(db)
        success = await keyword_repo.delete(keyword_id)
        if not success:
            raise HTTPException(status_code=404, detail="Keyword not found")
        return {"message": "Keyword deleted successfully"}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )


# Visual content routes

# @interactive_content_router.post("/visuals")
# async def create_visual_item(
#     visual_data: VisualItemCreateSchema,
#     db: AsyncSession = Depends(get_db_session)
# ):
#     """
#     Create a new visual item.
#     """
#     try:
#         visual_repo = VisualItemRepository(db)
#         visual = await visual_repo.create(visual_data.model_dump())
#         return {"results": visual}
#     except CustomException as e:
#         raise CustomHTTPException(
#             status_code=e.status_code,
#             detail=e.detail,
#             exception_type=e.exception_type,
#             additional_info=e.additional_info,
#         )
#     except Exception as e:
#         raise CustomHTTPException(
#             status_code=500,
#             detail="Internal server error",
#             exception_type="InternalServerError",
#             additional_info={"error": str(e)},
#         )


# Visual endpoints

@interactive_content_router.get("/paragraphs/{paragraph_id}/visual")
async def get_visual_by_paragraph(
    paragraph_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get the visual item for a specific paragraph.
    """
    try:
        visual_repo = VisualItemRepository(db)
        visual = await visual_repo.get_visual_by_paragraph_id(paragraph_id)
        return {"results": visual}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )
    

@interactive_content_router.put("/visuals/{visual_id}")
async def update_visual_data(
    visual_id: uuid.UUID,
    visual_update: VisualDataUpdateSchema,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Update visual data.
    """
    try:
        visual_repo = VisualItemRepository(db)
        
        update_data = {}
        if visual_update.visual_type is not None:
            # Need to get visual type ID by name
            visual_type_repo = VisualTypeRepository(db)
            visual_type = await visual_type_repo.get_by_name(visual_update.visual_type.value)
            if not visual_type:
                raise HTTPException(status_code=400, detail=f"Visual type {visual_update.visual_type.value} not found")
            update_data["visual_type_id"] = visual_type.id
            
        if visual_update.start_time is not None:
            update_data["start_time"] = visual_update.start_time
            
        # Handle table/chart/image data updates would require more complex logic
        # For now, updating basic fields only
            
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
            
        visual = await visual_repo.update(visual_id, update_data)
        if not visual:
            raise HTTPException(status_code=404, detail="Visual item not found")
            
        return {"results": visual}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )


@interactive_content_router.delete("/visuals/{visual_id}")
async def delete_visual_data(
    visual_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Delete visual data.
    """
    try:
        visual_repo = VisualItemRepository(db)
        success = await visual_repo.delete(visual_id)
        if not success:
            raise HTTPException(status_code=404, detail="Visual item not found")
        return {"message": "Visual item deleted successfully"}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )

# Table data routes
# @interactive_content_router.post("/tables")
# async def create_table(
#     table_data: TableDataCreateSchema,
#     db: AsyncSession = Depends(get_db_session)
# ):
#     """
#     Create a new table data.
#     """
#     try:
#         table_repo = TableDataRepository(db)
#         table = await table_repo.create(table_data.model_dump())
#         return {"results": table}
#     except CustomException as e:
#         raise CustomHTTPException(
#             status_code=e.status_code,
#             detail=e.detail,
#             exception_type=e.exception_type,
#             additional_info=e.additional_info,
#         )
#     except Exception as e:
#         raise CustomHTTPException(
#             status_code=500,
#             detail="Internal server error",
#             exception_type="InternalServerError",
#             additional_info={"error": str(e)},
#         )


# Chart data routes
# @interactive_content_router.post("/charts")
# async def create_chart(
#     chart_data: ChartDataCreateSchema,
#     db: AsyncSession = Depends(get_db_session)
# ):
#     """
#     Create a new chart data.
#     """
#     try:
#         chart_repo = ChartDataRepository(db)
#         chart = await chart_repo.create(chart_data.model_dump())
#         return {"results": chart}
#     except CustomException as e:
#         raise CustomHTTPException(
#             status_code=e.status_code,
#             detail=e.detail,
#             exception_type=e.exception_type,
#             additional_info=e.additional_info,
#         )
#     except Exception as e:
#         raise CustomHTTPException(
#             status_code=500,
#             detail="Internal server error",
#             exception_type="InternalServerError",
#             additional_info={"error": str(e)},
#         )


# # Image routes
# @interactive_content_router.post("/images")
# async def create_image(
#     image_data: ImageCreateSchema,
#     db: AsyncSession = Depends(get_db_session)
# ):
#     """
#     Create a new image.
#     """
#     try:
#         image_repo = ImageRepository(db)
#         image = await image_repo.create(image_data.model_dump())
#         return {"results": image}
#     except CustomException as e:
#         raise CustomHTTPException(
#             status_code=e.status_code,
#             detail=e.detail,
#             exception_type=e.exception_type,
#             additional_info=e.additional_info,
#         )
#     except Exception as e:
#         raise CustomHTTPException(
#             status_code=500,
#             detail="Internal server error",
#             exception_type="InternalServerError",
#             additional_info={"error": str(e)},
#         )


# Word endpoints

@interactive_content_router.post("/word-types")
async def create_word_type(
    word_type_data: WordTypeCreateSchema,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Create a new word type.
    """
    try:
        word_type_repo = WordTypeRepository(db)
        async with db.begin():
            word_type = await word_type_repo.create(word_type_data.model_dump())
        return {"results": word_type}
    except CustomException as e:
        raise CustomHTTPException(
            status_code=e.status_code,
            detail=e.detail,
            exception_type=e.exception_type,
            additional_info=e.additional_info,
        )
    except Exception as e:
        raise CustomHTTPException(
            status_code=500,
            detail="Internal server error",
            exception_type="InternalServerError",
            additional_info={"error": str(e)},
        )
