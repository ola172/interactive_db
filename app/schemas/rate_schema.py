from pydantic import BaseModel, Field
import uuid

class ProductRatingCreate(BaseModel):
    product_id: uuid.UUID
    rating: int = Field(..., ge=1, le=5)
    review: str | None = None

