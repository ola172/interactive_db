import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.user import UserRole, EnrollmentStatus, WaitingStatus


class UserBase(BaseModel):
    name: str
    email: str
    role: Optional[UserRole] = UserRole.student
    is_active: Optional[bool] = True
    is_verified: Optional[bool] = False


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: uuid.UUID
    profile_image: Optional[str] = None
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class UserProductSchema(BaseModel):
    product_id: uuid.UUID
    enrolled_at: Optional[datetime] = None
    progress: float = 0.0
    status: EnrollmentStatus = EnrollmentStatus.in_progress
    is_like: bool = False


class UserWaitingListSchema(BaseModel):
    product_id: uuid.UUID
    status: WaitingStatus = WaitingStatus.waiting
    created_at: Optional[datetime] = None
