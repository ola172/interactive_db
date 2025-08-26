# Product-related routes
import uuid

from fastapi import APIRouter, Depends, Query

from app.container import get_instructor_service
from app.schemas.instructor import InstructorBase
from app.services.instructor_service import InstructorService

instructor_router = APIRouter(prefix="/instructors", tags=["instructors"])


@instructor_router.post("")
async def create_instructor(
    instructor_request: InstructorBase,
    instructor_service: InstructorService = Depends(get_instructor_service)
):
    return await instructor_service.create_instructor(instructor_request)


@instructor_router.get("/all")
async def get_all_instructors(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    instructor_service: InstructorService = Depends(get_instructor_service)
):
    return await instructor_service.get_all_instructors(page, limit)

@instructor_router.get("/{instructor_id}")
async def get_instructor_by_id(
    instructor_id: uuid.UUID,
    instructor_service: InstructorService = Depends(get_instructor_service)
):
    return await instructor_service.get_instructor_by_id(instructor_id)

