import uuid
from fastapi import APIRouter, Depends, Query, HTTPException

from app.container import get_interactive_course_service
from app.exceptions.custom_exception import CustomHTTPException, CustomException
from app.schemas.interactive_schemas import (
    InteractiveCourseCreateSchema,
    InteractiveCourseUpdateSchema,
    InteractiveChapterCreateSchema,
    InteractiveChapterUpdateSchema,
    InteractiveVideoCreateSchema,
)
from app.services.interactive_course_service import InteractiveCourseService

interactive_course_router = APIRouter(prefix="/interactive-courses", tags=["Interactive Courses"])


# Course Endpoints

@interactive_course_router.post("/")
async def create_interactive_course(
    course_request: InteractiveCourseCreateSchema,
    interactive_course_service: InteractiveCourseService = Depends(get_interactive_course_service)
):
    """
    Create a new interactive course product with chapters and videos.
    """
    try:
        result = await interactive_course_service.create_interactive_course_product(course_request)
        return result
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


@interactive_course_router.get("/all")
async def get_all_interactive_courses(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    category_id: uuid.UUID | None = None,
    skill_id: uuid.UUID | None = None,
    interactive_course_service: InteractiveCourseService = Depends(get_interactive_course_service)
):
    """
    Get all interactive courses with optional pagination and filtering.
    """
    try:
        courses = await interactive_course_service.get_all_interactive_courses(
            page=page, 
            limit=limit,
            category_id=category_id,
            skill_id=skill_id
        )
        return {"results": courses}
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


@interactive_course_router.get("/{product_id}")
async def get_interactive_course_by_id(
    product_id: uuid.UUID,
    interactive_course_service: InteractiveCourseService = Depends(get_interactive_course_service)
):
    """
    Get an interactive course by its product ID.
    """
    try:
        result = await interactive_course_service.get_interactive_course_product(product_id=product_id)
        if not result:
            raise HTTPException(status_code=404, detail="Interactive course not found")
        return {"results": result}
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


@interactive_course_router.put("/{product_id}")
async def update_interactive_course(
    product_id: uuid.UUID,
    course_update: InteractiveCourseUpdateSchema,
    interactive_course_service: InteractiveCourseService = Depends(get_interactive_course_service)
):
    """
    Update an interactive course by its product ID.
    """
    try:
        success = await interactive_course_service.update_interactive_course_product(product_id, course_update)
        if success:
            return {"message": "Interactive course updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Interactive course not found")
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


@interactive_course_router.delete("/{product_id}")
async def delete_interactive_course(
    product_id: uuid.UUID,
    interactive_course_service: InteractiveCourseService = Depends(get_interactive_course_service)
):
    """
    Delete an interactive course by its product ID.
    """
    try:
        success = await interactive_course_service.delete_interactive_course_product(product_id)
        if success:
            return {"message": "Interactive course deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Interactive course not found")
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


# Chapter Endpoints

@interactive_course_router.get("/{course_id}/chapters")
async def get_chapters_by_course(
    course_id: uuid.UUID,
    interactive_course_service: InteractiveCourseService = Depends(get_interactive_course_service)
):
    """
    Get all chapters for a specific interactive course.
    """
    try:
        chapters = await interactive_course_service.chapter_repo.get_chapters_by_course_id(course_id)
        return {"results": chapters}
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


@interactive_course_router.post("/chapters")
async def create_chapter(
    chapter_data: InteractiveChapterCreateSchema,
    interactive_course_service: InteractiveCourseService = Depends(get_interactive_course_service)
):
    """
    Create a new chapter for an interactive course.
    """
    try:
        chapter = await interactive_course_service.create_chapter(chapter_data)
        return {"results": chapter}
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


@interactive_course_router.put("/chapters/{chapter_id}")
async def update_chapter(
    chapter_id: uuid.UUID,
    chapter_update: InteractiveChapterUpdateSchema,
    interactive_course_service: InteractiveCourseService = Depends(get_interactive_course_service)
):
    """
    Update a chapter by its ID.
    """
    try:
        chapter = await interactive_course_service.update_chapter(chapter_id, chapter_update)
        return {"results": chapter}
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


@interactive_course_router.delete("/chapters/{chapter_id}")
async def delete_chapter(
    chapter_id: uuid.UUID,
    interactive_course_service: InteractiveCourseService = Depends(get_interactive_course_service)
):
    """
    Delete a chapter by its ID.
    """
    try:
        success = await interactive_course_service.delete_chapter(chapter_id)
        if success:
            return {"message": "Chapter deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Chapter not found")
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


@interactive_course_router.get("/chapters/{chapter_id}/videos")
async def get_videos_by_chapter(
    chapter_id: uuid.UUID,
    interactive_course_service: InteractiveCourseService = Depends(get_interactive_course_service)
):
    """
    Get all videos for a specific chapter.
    """
    try:
        videos = await interactive_course_service.video_repo.get_videos_by_chapter_id(chapter_id)
        return {"results": videos}
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


# Videos Endpoints

@interactive_course_router.post("/videos")
async def create_video(
    video_data: InteractiveVideoCreateSchema,
    interactive_course_service: InteractiveCourseService = Depends(get_interactive_course_service)
):
    """
    Create a new video for an interactive chapter.
    """
    try:
        video = await interactive_course_service.create_video(video_data.model_dump())
        return {"results": video}
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


@interactive_course_router.get("/videos/{video_id}")
async def get_video_with_paragraphs(
    video_id: uuid.UUID,
    interactive_course_service: InteractiveCourseService = Depends(get_interactive_course_service)
):
    """
    Get a video with its paragraphs and interactive content.
    """
    try:
        video = await interactive_course_service.video_repo.get_video_with_paragraphs(video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        return {"results": video}
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