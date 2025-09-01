import uuid
from fastapi import APIRouter, Depends, Query

from app.container import get_course_service
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
    course_id = await course_service.create_course_product(course_request)
    return {"course_id": course_id}


@course_router.get("/all")
async def get_all_courses(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    category_id: uuid.UUID | None = None,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Get all courses with optional pagination.
    """
    return await course_service.get_all_courses(page=page, limit=limit, category_id=category_id)

@course_router.get("/{product_id}")
async def get_course_by_id(
    product_id: uuid.UUID,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Get a course by its product ID.
    """
    return await course_service.get_course_product(product_id=product_id)


@course_router.delete("/{product_id}")
async def delete_course(
    product_id: uuid.UUID,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Delete a course by its ID.
    """
    return await course_service.delete_course_product(product_id=product_id)
