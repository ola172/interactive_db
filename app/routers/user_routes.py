import uuid
from fastapi import APIRouter, Depends

from app.container import get_user_service
from app.exceptions.custom_exception import CustomHTTPException, CustomException
from app.schemas.rate_schema import ProductRatingCreate, InstructorRatingCreate
from app.schemas.user_schema import UserCreate, UserProductSchema, UserWaitingListSchema
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("")
async def create_user(user_request: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        user_id = await service.create_user(user_request)
        return {"user_id": user_id}
    except CustomException as e:
        raise CustomHTTPException(status_code=e.status_code, detail=e.detail,
                                  exception_type=e.exception_type, additional_info=e.additional_info)


@router.post("/{user_id}/enroll")
async def enroll_user(user_id: uuid.UUID, product: UserProductSchema, service: UserService = Depends(get_user_service)):
    try:
        return await service.enroll_user_to_product(user_id, product)
    except CustomException as e:
        raise CustomHTTPException(status_code=e.status_code, detail=e.detail,
                                  exception_type=e.exception_type, additional_info=e.additional_info)


@router.post("/{user_id}/waiting-list")
async def add_user_waiting_list(user_id: uuid.UUID, product: UserWaitingListSchema,
                                service: UserService = Depends(get_user_service)):
    try:
        return await service.add_to_waiting_list(user_id, product)
    except CustomException as e:
        raise CustomHTTPException(status_code=e.status_code, detail=e.detail,
                                  exception_type=e.exception_type, additional_info=e.additional_info)


@router.get("/all")
async def get_all_users(service: UserService = Depends(get_user_service)):
    try:
        results = await service.get_all_users()
        return {"results": results}
    except CustomException as e:
        raise CustomHTTPException(status_code=e.status_code, detail=e.detail,
                                  exception_type=e.exception_type, additional_info=e.additional_info)


@router.get("/{user_id}")
async def get_user(user_id: uuid.UUID, service: UserService = Depends(get_user_service)):
    try:
        results = await service.get_user_with_enrollments(user_id)
        return {"results": results}
    except CustomException as e:
        raise CustomHTTPException(status_code=e.status_code, detail=e.detail,
                                  exception_type=e.exception_type, additional_info=e.additional_info)


@router.get("/{user_id}/product-status/{product_id}")
async def get_product_status(user_id: uuid.UUID, product_id: uuid.UUID,
                             service: UserService = Depends(get_user_service)):
    try:
        return await service.get_product_status_for_user(user_id, product_id)
    except CustomException as e:
        raise CustomHTTPException(status_code=e.status_code, detail=e.detail,
                                  exception_type=e.exception_type, additional_info=e.additional_info)


@router.delete("/{user_id}/waiting-list/{product_id}")
async def remove_user_waiting_list(user_id: uuid.UUID, product_id: uuid.UUID,
                                   service: UserService = Depends(get_user_service)):
    try:
        entry = await service.remove_from_waiting_list(user_id, product_id)
        if entry:
            return {"removed": True, "product_id": str(product_id)}
        return {"removed": False, "product_id": str(product_id)}
    except CustomException as e:
        raise CustomHTTPException(status_code=e.status_code, detail=e.detail,
                                  exception_type=e.exception_type, additional_info=e.additional_info)


@router.post("/{user_id}/product-rating")
async def add_or_update_rating(
        user_id: uuid.UUID,
        rating_data: ProductRatingCreate,
        service: UserService = Depends(get_user_service)
):
    try:
        rating = await service.add_or_update_product_rating(
            user_id=user_id,
            product_id=rating_data.product_id,
            rating=rating_data.rating,
            review=rating_data.review
        )
        return rating
    except CustomException as e:
        raise CustomHTTPException(status_code=e.status_code, detail=e.detail,
                                  exception_type=e.exception_type, additional_info=e.additional_info)


@router.post("/{user_id}/instructor-rating")
async def add_or_update_instructor_rating(
        user_id: uuid.UUID,
        rating_data: InstructorRatingCreate,
        service: UserService = Depends(get_user_service)
):
    try:
        rating = await service.add_or_update_instructor_rating(
            user_id=user_id,
            instructor_id=rating_data.instructor_id,
            rating=rating_data.rating,
            review=rating_data.review
        )
        return rating
    except CustomException as e:
        raise CustomHTTPException(status_code=e.status_code, detail=e.detail,
                                  exception_type=e.exception_type, additional_info=e.additional_info)


@router.get('/enroll-num/{product_id}')
async def number_of_student(product_id: uuid.UUID, service: UserService = Depends(get_user_service)):
    try:
        number = await service.number_of_student(product_id)
        return {"student_number": number}
    except CustomException as e:
        raise CustomHTTPException(status_code=e.status_code, detail=e.detail,
                                  exception_type=e.exception_type, additional_info=e.additional_info)