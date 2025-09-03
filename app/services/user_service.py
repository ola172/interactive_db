import uuid
from typing import Optional

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import User, UserProduct, UserWaitingList, ProductRating
from app.models.user import EnrollmentStatus
from app.repositories.instructor import InstructorRateRepository
from app.repositories.user import (
    UserRepository,
    UserProductRepository,
    UserWaitingListRepository,
)
from app.schemas.user_schema import UserCreate, UserProductSchema, UserWaitingListSchema
from app.exceptions.custom_exception import CustomException
from app.exceptions.service_exception import ServiceException


class UserService:
    def __init__(
        self,
        db,
        user_repo: UserRepository,
        user_product_repo: UserProductRepository,
        instructor_rate_repo: InstructorRateRepository,
        waiting_repo: UserWaitingListRepository,
    ):
        self.db = db
        self.user_repo = user_repo
        self.user_product_repo = user_product_repo
        self.waiting_repo = waiting_repo
        self.instructor_rate_repo = instructor_rate_repo

    async def create_user(self, user_data: UserCreate) -> uuid.UUID:
        try:
            async with self.db.begin():
                user = await self.user_repo.create(
                    {
                        "name": user_data.name,
                        "email": user_data.email,
                        "password_hash": user_data.password,
                        "role": user_data.role,
                    }
                )
            return user.id
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to create user",
                additional_info={"error": str(e), "email": user_data.email},
            )

    async def enroll_user_to_product(
        self, user_id: uuid.UUID, product: UserProductSchema
    ):
        """
        Enroll a user to a product (course/book/pathway) or update existing enrollment.
        """
        try:
            async with self.db.begin():
                stmt = select(UserProduct).where(
                    UserProduct.user_id == user_id,
                    UserProduct.product_id == product.product_id,
                )
                result = await self.db.execute(stmt)
                enrollment = result.scalar_one_or_none()

                if enrollment:
                    enrollment.progress = product.progress
                    enrollment.status = product.status
                    enrollment.is_like = product.is_like
                    await self.db.flush()
                    return enrollment
                else:
                    return await self.user_product_repo.create(
                        {
                            "user_id": user_id,
                            "product_id": product.product_id,
                            "progress": product.progress,
                            "status": product.status or EnrollmentStatus.in_progress,
                            "is_like": product.is_like,
                        }
                    )
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to enroll user to product",
                additional_info={
                    "error": str(e),
                    "user_id": str(user_id),
                    "product_id": str(product.product_id),
                },
            )

    async def add_to_waiting_list(
        self, user_id: uuid.UUID, product: UserWaitingListSchema
    ):
        """
        Add a user to a product's waiting list.
        """
        try:
            async with self.db.begin():
                return await self.waiting_repo.create(
                    {
                        "user_id": user_id,
                        "product_id": product.product_id,
                        "status": product.status,
                    }
                )
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to add user to waiting list",
                additional_info={
                    "error": str(e),
                    "user_id": str(user_id),
                    "product_id": str(product.product_id),
                },
            )

    async def get_user_with_enrollments(self, user_id: uuid.UUID):
        """
        Return user info along with all enrolled products and waiting list items.
        """
        try:
            stmt = (
                select(User)
                .where(User.id == user_id)
                .options(
                    selectinload(User.enrollments).selectinload(UserProduct.product),
                    selectinload(User.waiting_list).selectinload(UserWaitingList.product),
                )
            )
            result = await self.db.execute(stmt)
            return result.scalar_one_or_none()
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch user with enrollments",
                additional_info={"error": str(e), "user_id": str(user_id)},
            )

    async def get_all_users(self):
        try:
            return await self.user_repo.get_all()
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch all users",
                additional_info={"error": str(e)},
            )

    async def get_product_status_for_user(
        self, user_id: uuid.UUID, product_id: uuid.UUID
    ):
        """
        Return enrollment and waiting status for a specific product for a user.
        """
        try:
            enrollment_stmt = (
                select(UserProduct)
                .where(
                    UserProduct.user_id == user_id,
                    UserProduct.product_id == product_id,
                )
            )
            enrollment_result = await self.db.execute(enrollment_stmt)
            enrollment = enrollment_result.scalar_one_or_none()

            return {
                "enrollment": {
                    "status": enrollment.status if enrollment else None,
                    "progress": enrollment.progress if enrollment else None,
                    "is_like": enrollment.is_like if enrollment else None,
                }
            }
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to fetch product status for user",
                additional_info={
                    "error": str(e),
                    "user_id": str(user_id),
                    "product_id": str(product_id),
                },
            )

    async def remove_from_waiting_list(
        self, user_id: uuid.UUID, product_id: uuid.UUID
    ):
        """
        Remove a user from waiting list for a specific product.
        """
        try:
            async with self.db.begin():
                stmt = select(UserWaitingList).where(
                    UserWaitingList.user_id == user_id,
                    UserWaitingList.product_id == product_id,
                )
                result = await self.db.execute(stmt)
                waiting_entry = result.scalar_one_or_none()
                if waiting_entry:
                    await self.waiting_repo.delete(waiting_entry.id)
                return waiting_entry
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to remove user from waiting list",
                additional_info={
                    "error": str(e),
                    "user_id": str(user_id),
                    "product_id": str(product_id),
                },
            )

    async def add_or_update_product_rating(
        self,
        user_id: uuid.UUID,
        product_id: uuid.UUID,
        rating: float,
        review: Optional[str] = None,
    ):
        """
        Add or update a user's rating and review for a product.
        """
        try:
            async with self.db.begin():
                stmt = select(ProductRating).where(
                    ProductRating.user_id == user_id,
                    ProductRating.product_id == product_id,
                )
                result = await self.db.execute(stmt)
                existing = result.scalar_one_or_none()

                if existing:
                    existing.rating = rating
                    existing.review = review
                    await self.db.flush()
                    return existing
                else:
                    new_rating = ProductRating(
                        user_id=user_id,
                        product_id=product_id,
                        rating=rating,
                        review=review,
                    )
                    self.db.add(new_rating)
                    await self.db.flush()
                    return new_rating
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to add or update product rating",
                additional_info={
                    "error": str(e),
                    "user_id": str(user_id),
                    "product_id": str(product_id),
                    "rating": rating,
                    "review": review,
                },
            )

    async def add_or_update_instructor_rating(
        self,
        user_id: uuid.UUID,
        instructor_id: uuid.UUID,
        rating: float,
        review: Optional[str] = None,
    ):
        """
        Add or update a user's rating and review for an instructor.
        """
        try:
            async with self.db.begin():
                stmt = select(self.instructor_rate_repo.model).where(
                    self.instructor_rate_repo.model.user_id == user_id,
                    self.instructor_rate_repo.model.instructor_id == instructor_id,
                )
                result = await self.db.execute(stmt)
                existing = result.scalar_one_or_none()

                if existing:
                    existing.rating = rating
                    existing.review = review
                    await self.db.flush()
                    return existing
                else:
                    new_rating = self.instructor_rate_repo.model(
                        user_id=user_id,
                        instructor_id=instructor_id,
                        rating=rating,
                        review=review,
                    )
                    self.db.add(new_rating)
                    await self.db.flush()
                    return new_rating
        except CustomException as e:
            raise e
        except Exception as e:
            raise ServiceException(
                status_code=500,
                detail="Failed to add or update instructor rating",
                additional_info={
                    "error": str(e),
                    "user_id": str(user_id),
                    "instructor_id": str(instructor_id),
                    "rating": rating,
                    "review": review,
                },
            )
