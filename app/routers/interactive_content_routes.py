import uuid
from fastapi import APIRouter, Depends

from app.container import get_interactive_content_service
from app.exceptions.custom_exception import CustomHTTPException, CustomException

from app.schemas.interactive_schemas import (
    InteractiveKeywordUpdateSchema,
    VisualDataUpdateSchema,
    VisualDataCreateSchema,
    KeyWordTypeCreateSchema,
    KeyWordTypeUpdateSchema,
    InteractiveKeywordCreateSchema,
    WordTypeCreateSchema,
    WordTypeUpdateSchema,
    VisualTypeCreateSchema,
    VisualTypeUpdateSchema,
    ChartTypeCreateSchema,
    ChartTypeUpdateSchema,
)
from app.services.interactive_content_service import InteractiveContentService

interactive_content_router = APIRouter(
    prefix="/interactive_content", tags=["Interactive Content"]
)


# Paragraph routes


@interactive_content_router.get("/videos/{video_id}/paragraphs/")
async def get_paragraphs_by_video(
    video_id: uuid.UUID,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Get all paragraphs for a specific video with interactive content.
    """
    try:
        paragraphs = await interactive_content_service.get_paragraphs_by_video(video_id)
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


# Keyword routes


@interactive_content_router.post("/keyword_types/")
async def create_keyword_type(
    keyword_type_data: KeyWordTypeCreateSchema,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Create a new keyword type.
    """
    try:
        keyword_type = await interactive_content_service.create_keyword_type(
            keyword_type_data
        )
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


@interactive_content_router.post("/paragraphs/{paragraph_id}/keywords/")
async def create_keyword(
    paragraph_id: uuid.UUID,
    keyword_data: InteractiveKeywordCreateSchema,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Create a new interactive keyword for a specific paragraph.
    """
    try:
        keyword = await interactive_content_service.create_keyword(
            paragraph_id, keyword_data
        )
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


@interactive_content_router.put("/keywords/{keyword_id}/")
async def update_keyword(
    keyword_id: uuid.UUID,
    keyword_update: InteractiveKeywordUpdateSchema,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Update keyword (name, type, style).
    """
    try:
        keyword = await interactive_content_service.update_keyword(
            keyword_id, keyword_update
        )
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


@interactive_content_router.delete("/keywords/{keyword_id}/")
async def delete_keyword(
    keyword_id: uuid.UUID,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Delete a keyword item.
    """
    try:
        success = await interactive_content_service.delete_keyword(keyword_id)
        return {"message": "Keyword deleted successfully"}
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


# Visual endpoints


@interactive_content_router.post("/paragraphs/{paragraph_id}/visual/")
async def create_visual_data(
    paragraph_id: uuid.UUID,
    visual_data: VisualDataCreateSchema,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Create visual data for a paragraph using registry pattern.
    """
    try:
        visual = await interactive_content_service.create_visual_data(
            paragraph_id, visual_data
        )
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


@interactive_content_router.get("/visuals/{visual_id}/")
async def get_visual_data_by_id(
    visual_id: uuid.UUID,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Get visual data by visual_id with full content.
    """
    try:
        visual_data = await interactive_content_service.get_visual_data_by_id(visual_id)
        return {"results": visual_data}
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


@interactive_content_router.put("/visuals/{visual_id}/")
async def update_visual_data(
    visual_id: uuid.UUID,
    visual_update: VisualDataUpdateSchema,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Update visual data.
    """
    try:
        visual = await interactive_content_service.update_visual_data(
            visual_id, visual_update
        )
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


@interactive_content_router.delete("/visuals/{visual_id}/")
async def delete_visual_data(
    visual_id: uuid.UUID,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Delete visual data.
    """
    try:
        success = await interactive_content_service.delete_visual_data(visual_id)
        return {"message": "Visual item deleted successfully"}
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


# Word endpoints


@interactive_content_router.post("/word_types/")
async def create_word_type(
    word_type_data: WordTypeCreateSchema,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Create a new word type.
    """
    try:
        word_type = await interactive_content_service.create_word_type(word_type_data)
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


# Video keyword style endpoints


@interactive_content_router.get("/videos/{video_id}/keyword-styles/")
async def get_video_keyword_styles(
    video_id: uuid.UUID,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Get all keyword styles for a specific video.
    """
    try:
        styles = await interactive_content_service.get_video_keyword_styles(video_id)
        return {"results": styles}
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


# Type endpoints


@interactive_content_router.get("/keyword-types/")
async def get_keyword_types(
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Get all available keyword types.
    """
    try:
        keyword_types = await interactive_content_service.get_all_keyword_types()
        return {"results": keyword_types}
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


@interactive_content_router.get("/word-types/")
async def get_word_types(
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Get all available word types.
    """
    try:
        word_types = await interactive_content_service.get_all_word_types()
        return {"results": word_types}
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


@interactive_content_router.get("/visual-types/")
async def get_visual_types(
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Get all available visual types.
    """
    try:
        visual_types = await interactive_content_service.get_all_visual_types()
        return {"results": visual_types}
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


@interactive_content_router.get("/chart-types/")
async def get_chart_types(
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Get all available chart types.
    """
    try:
        chart_types = await interactive_content_service.get_all_chart_types()
        return {"results": chart_types}
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


# Keyword Type CRUD endpoints


@interactive_content_router.put("/keyword_types/{keyword_type_id}/")
async def update_keyword_type(
    keyword_type_id: uuid.UUID,
    keyword_type_update: KeyWordTypeUpdateSchema,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Update keyword type (name, description).
    """
    try:
        keyword_type = await interactive_content_service.update_keyword_type(
            keyword_type_id, keyword_type_update
        )
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


@interactive_content_router.delete("/keyword_types/{keyword_type_id}/")
async def delete_keyword_type(
    keyword_type_id: uuid.UUID,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Delete a keyword type.
    """
    try:
        success = await interactive_content_service.delete_keyword_type(keyword_type_id)
        return {"message": "Keyword type deleted successfully"}
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


# Word Type CRUD endpoints


@interactive_content_router.put("/word_types/{word_type_id}/")
async def update_word_type(
    word_type_id: uuid.UUID,
    word_type_update: WordTypeUpdateSchema,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Update word type (name, description).
    """
    try:
        word_type = await interactive_content_service.update_word_type(
            word_type_id, word_type_update
        )
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


@interactive_content_router.delete("/word_types/{word_type_id}/")
async def delete_word_type(
    word_type_id: uuid.UUID,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Delete a word type.
    """
    try:
        success = await interactive_content_service.delete_word_type(word_type_id)
        return {"message": "Word type deleted successfully"}
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


# Visual Type CRUD endpoints


@interactive_content_router.post("/visual_types/")
async def create_visual_type(
    visual_type_data: VisualTypeCreateSchema,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Create a new visual type.
    """
    try:
        visual_type = await interactive_content_service.create_visual_type(
            visual_type_data
        )
        return {"results": visual_type}
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


@interactive_content_router.put("/visual_types/{visual_type_id}/")
async def update_visual_type(
    visual_type_id: uuid.UUID,
    visual_type_update: VisualTypeUpdateSchema,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Update visual type (name, description).
    """
    try:
        visual_type = await interactive_content_service.update_visual_type(
            visual_type_id, visual_type_update
        )
        return {"results": visual_type}
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


@interactive_content_router.delete("/visual_types/{visual_type_id}/")
async def delete_visual_type(
    visual_type_id: uuid.UUID,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Delete a visual type.
    """
    try:
        success = await interactive_content_service.delete_visual_type(visual_type_id)
        return {"message": "Visual type deleted successfully"}
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


# Chart Type CRUD endpoints


@interactive_content_router.post("/chart_types/")
async def create_chart_type(
    chart_type_data: ChartTypeCreateSchema,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Create a new chart type.
    """
    try:
        chart_type = await interactive_content_service.create_chart_type(
            chart_type_data
        )
        return {"results": chart_type}
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


@interactive_content_router.put("/chart_types/{chart_type_id}/")
async def update_chart_type(
    chart_type_id: uuid.UUID,
    chart_type_update: ChartTypeUpdateSchema,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Update chart type (name, description).
    """
    try:
        chart_type = await interactive_content_service.update_chart_type(
            chart_type_id, chart_type_update
        )
        return {"results": chart_type}
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


@interactive_content_router.delete("/chart_types/{chart_type_id}/")
async def delete_chart_type(
    chart_type_id: uuid.UUID,
    interactive_content_service: InteractiveContentService = Depends(
        get_interactive_content_service
    ),
):
    """
    Delete a chart type.
    """
    try:
        success = await interactive_content_service.delete_chart_type(chart_type_id)
        return {"message": "Chart type deleted successfully"}
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
