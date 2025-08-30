import uuid

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import User, UserProduct, UserWaitingList, ProductRating
from app.repositories.user import UserRepository, UserProductRepository, UserWaitingListRepository
from app.schemas.user_schema import UserCreate, UserProductSchema, UserWaitingListSchema


class UserService:
    def __init__(self, db, user_repo: UserRepository,
                 user_product_repo: UserProductRepository,
                 waiting_repo: UserWaitingListRepository):
        self.db = db
        self.user_repo = user_repo
        self.user_product_repo = user_product_repo
        self.waiting_repo = waiting_repo

    async def create_user(self, user_data: UserCreate) -> uuid.UUID:
        async with self.db.begin():
            user = await self.user_repo.create({
                "name": user_data.name,
                "email": user_data.email,
                "password_hash": user_data.password,
                "role": user_data.role
            })
        return user.id

    async def enroll_user_to_product(self, user_id: uuid.UUID, product: UserProductSchema):
        async with self.db.begin():
            return await self.user_product_repo.create({
                "user_id": user_id,
                "product_id": product.product_id,
                "progress": product.progress,
                "status": product.status,
                "is_like": product.is_like
            })

    async def add_to_waiting_list(self, user_id: uuid.UUID, product: UserWaitingListSchema):
        async with self.db.begin():
            return await self.waiting_repo.create({
                "user_id": user_id,
                "product_id": product.product_id,
                "status": product.status
            })

    async def get_user_with_enrollments(self, user_id: uuid.UUID):
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.enrollments).selectinload(UserProduct.product),
                selectinload(User.waiting_list).selectinload(UserWaitingList.product)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_users(self):
        stmt = select(User)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_product_status_for_user(self, user_id: uuid.UUID, product_id: uuid.UUID):
        """
        Return enrollment and waiting status for a specific product for a user.
        """
        # check enrollment
        enrollment_stmt = (
            select(UserProduct)
            .where(UserProduct.user_id == user_id, UserProduct.product_id == product_id)
        )
        enrollment_result = await self.db.execute(enrollment_stmt)
        enrollment = enrollment_result.scalar_one_or_none()

        # check waiting list
        waiting_stmt = (
            select(UserWaitingList)
            .where(UserWaitingList.user_id == user_id, UserWaitingList.product_id == product_id)
        )
        waiting_result = await self.db.execute(waiting_stmt)
        waiting = waiting_result.scalar_one_or_none()

        return {
            "enrollment": {
                "status": enrollment.status if enrollment else None,
                "progress": enrollment.progress if enrollment else None,
                "is_like": enrollment.is_like if enrollment else None,
            },
            "waiting_list": {
                "status": waiting.status if waiting else None,
                "created_at": waiting.created_at if waiting else None,
            }
        }

    async def remove_from_waiting_list(self, user_id: uuid.UUID, product_id: uuid.UUID):
        """
        Remove a user from waiting list for a specific product.
        """
        async with self.db.begin():
            waiting_stmt = (
                select(UserWaitingList)
                .where(UserWaitingList.user_id == user_id, UserWaitingList.product_id == product_id)
            )
            result = await self.db.execute(waiting_stmt)
            waiting_entry = result.scalar_one_or_none()
            if waiting_entry:
                await self.waiting_repo.delete(waiting_entry.id)
            return waiting_entry

    async def add_or_update_product_rating(self, user_id: uuid.UUID, product_id: uuid.UUID, rating: int,
                                           review: str = None):
        """
        Add or update a user's rating and review for a product.
        """
        async with self.db.begin():
            # Check if rating exists
            stmt = select(ProductRating).where(
                ProductRating.user_id == user_id,
                ProductRating.product_id == product_id
            )
            result = await self.db.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                # Update existing rating
                existing.rating = rating
                existing.review = review
                await self.db.flush()
                return existing
            else:
                # Create new rating
                new_rating = ProductRating(
                    user_id=user_id,
                    product_id=product_id,
                    rating=rating,
                    review=review
                )
                self.db.add(new_rating)
                await self.db.flush()
                return new_rating