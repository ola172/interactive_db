from pydantic import BaseModel, Field
import uuid

class ProductRatingCreate(BaseModel):
    product_id: uuid.UUID
    rating: float = Field(ge=1, le=5)  # rating between 1 and 5
    review: str | None = None


class InstructorRatingCreate(BaseModel):
    instructor_id: uuid.UUID
    rating: float = Field(ge=1, le=5)  # rating between 1 and 5
    review: str | None = None