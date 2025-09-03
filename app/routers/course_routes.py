import uuid
from fastapi import APIRouter, Depends, Query

from app.container import get_course_service
from app.exceptions.custom_exception import CustomHTTPException, CustomException
from app.schemas.course import CourseDetailSchema
from app.services import CourseService

course_router = APIRouter(prefix="/courses", tags=["Courses"])


@course_router.post("")
async def create_course(
    course_request: CourseDetailSchema,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Create a new course product with chapters and videos.
    """
    try:
        course_id = await course_service.create_course_product(course_request)
        return {"course_id": course_id}
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


@course_router.get("/all")
async def get_all_courses(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    category_id: uuid.UUID | None = None,
    instructor_id: uuid.UUID | None = None,
    skill_id: uuid.UUID | None = None,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Get all courses with optional pagination.
    """
    try:
        courses = await course_service.get_all_courses(page=page, limit=limit,
                                                       category_id=category_id,
                                                       instructor_id=instructor_id,
                                                       skill_id=skill_id)
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


@course_router.get("/{product_id}")
async def get_course_by_id(
    product_id: uuid.UUID,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Get a course by its product ID.
    """
    try:
        results = await course_service.get_course_product(product_id=product_id)
        return {"results": results}
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


@course_router.delete("/{product_id}")
async def delete_course(
    product_id: uuid.UUID,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Delete a course by its ID.
    """
    try:
        results = await course_service.delete_course_product(product_id=product_id)
        return {"results": results}
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
