import uuid
from fastapi import APIRouter, Depends, Query

from app.container import get_course_service
from app.schemas.course import CreateCourse, CourseCategoryBase
from app.services import CourseService

course_router = APIRouter(prefix="/courses", tags=["Courses"])


@course_router.post("")
async def create_course(
    course_request: CreateCourse,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Create a new course product with chapters and videos.
    """
    return await course_service.create_course_product(course_request)


@course_router.get("/product/{product_id}")
async def get_course_by_product(
    product_id: uuid.UUID,
    course_service: CourseService = Depends(get_course_service)
):
    """
    Get a course by its product ID, including chapters and videos.
    """
    return await course_service.get_course_product(product_id=product_id)


@course_router.get("/all")
async def get_all_courses(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    course_service: CourseService = Depends(get_course_service)
):
    """
    Get all courses with optional pagination.
    """
    return await course_service.get_all_courses(page=page, limit=limit)

@course_router.get("/category")
async def get_all_course_categories(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    course_service: CourseService = Depends(get_course_service)
):
    """
    Get all course categories with optional pagination.
    """
    return await course_service.get_all_course_categories(page=page, limit=limit)

@course_router.post("/categoryone")
async def create_course_category(
    category_request: CourseCategoryBase,
    course_service: CourseService = Depends(get_course_service)
):
    return await course_service.create_course_category(category_request)

