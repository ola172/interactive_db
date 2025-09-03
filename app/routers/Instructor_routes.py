# Product-related routes
import uuid

from fastapi import APIRouter, Depends, Query

from app.container import get_instructor_service
from app.exceptions.custom_exception import CustomHTTPException, CustomException
from app.schemas.instructor import InstructorBase
from app.services import instructor_service
from app.services.instructor_service import InstructorService

instructor_router = APIRouter(prefix="/instructors", tags=["instructors"])


@instructor_router.post("")
async def create_instructor(
    instructor_request: InstructorBase,
    instructor_service: InstructorService = Depends(get_instructor_service)
):
    try:
        return await instructor_service.create_instructor(instructor_request)
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


@instructor_router.get("/all")
async def get_all_instructors(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    instructor_service: InstructorService = Depends(get_instructor_service)
):
    try:
        results = await instructor_service.get_all_instructors(page, limit)
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


@instructor_router.get("/{instructor_id}")
async def get_instructor_by_id(
    instructor_id: uuid.UUID,
    instructor_service: InstructorService = Depends(get_instructor_service)
):
    try:
        results = await instructor_service.get_instructor_by_id(instructor_id)
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

@instructor_router.get("/average-rating/{instructor_id}")
async def get_rate_instructor_by_id(instructor_id: uuid.UUID,
                                    instructor_service: InstructorService = Depends(get_instructor_service)):
    results = await instructor_service.get_instructor_average_rating(instructor_id)
    return {"results": results}

@instructor_router.get("/rates/{instructor_id}")
async def get_instructor_rating(instructor_id: uuid.UUID, instructor_service: InstructorService = Depends(get_instructor_service)):
    results = await instructor_service.get_instructor_rating(instructor_id)
    return {"results": results}