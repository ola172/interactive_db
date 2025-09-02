import uuid
from fastapi import APIRouter, Depends

from app.container import get_user_service
from app.schemas.rate_schema import ProductRatingCreate
from app.schemas.user_schema import UserCreate, UserProductSchema, UserWaitingListSchema
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("")
async def create_user(user_request: UserCreate, service: UserService = Depends(get_user_service)):
    user_id = await service.create_user(user_request)
    return {"user_id": user_id}


@router.post("/{user_id}/enroll")
async def enroll_user(user_id: uuid.UUID, product: UserProductSchema, service: UserService = Depends(get_user_service)):
    return await service.enroll_user_to_product(user_id, product)


@router.post("/{user_id}/waiting-list")
async def add_user_waiting_list(user_id: uuid.UUID, product: UserWaitingListSchema,
                                service: UserService = Depends(get_user_service)):
    return await service.add_to_waiting_list(user_id, product)


@router.get("/all")
async def get_all_users(service: UserService = Depends(get_user_service)):
    results = await service.get_all_users()
    return {"results": results}

@router.get("/{user_id}")
async def get_user(user_id: uuid.UUID, service: UserService = Depends(get_user_service)):
    results = await service.get_user_with_enrollments(user_id)
    return {"results": results}


# ✅ Get status of a product for a user
@router.get("/{user_id}/product-status/{product_id}")
async def get_product_status(user_id: uuid.UUID, product_id: uuid.UUID,
                             service: UserService = Depends(get_user_service)):
    return await service.get_product_status_for_user(user_id, product_id)


# ✅ Remove from waiting list
@router.delete("/{user_id}/waiting-list/{product_id}")
async def remove_user_waiting_list(user_id: uuid.UUID, product_id: uuid.UUID,
                                   service: UserService = Depends(get_user_service)):
    entry = await service.remove_from_waiting_list(user_id, product_id)
    if entry:
        return {"removed": True, "product_id": str(product_id)}
    return {"removed": False, "product_id": str(product_id)}


# ✅ Add or update a rating for a product
@router.post("/{user_id}/ratings")
async def add_or_update_rating(
        user_id: uuid.UUID,
        rating_data: ProductRatingCreate,
        service: UserService = Depends(get_user_service)
):
    rating = await service.add_or_update_product_rating(
        user_id=user_id,
        product_id=rating_data.product_id,
        rating=rating_data.rating,
        review=rating_data.review
    )
    return rating
