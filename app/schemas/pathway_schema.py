import uuid
from typing import List, Optional
from pydantic import BaseModel, Field


class PathwayItemSchema(BaseModel):
    product_id: Optional[uuid.UUID]
    order_index: Optional[int]

class ProductCreateSchema(BaseModel):
    type_id: uuid.UUID
    category_id: Optional[uuid.UUID]
    title: str
    description: Optional[str]
    language: Optional[str]
    level: Optional[str]
    duration: Optional[int]
    price: Optional[float]
    cover: Optional[str]
    short_video: Optional[str]
    # Optional: skills and objectives by ID
    skills: List[uuid.UUID] = Field(default_factory=list)
    objectives: List[uuid.UUID] = Field(default_factory=list)

class PathwayCreateWithProduct(BaseModel):
    product: ProductCreateSchema  # ✅ Product details
    name: str
    description: Optional[str] = None
    items: List[PathwayItemSchema] = Field(default_factory=list)


class PathwayItemResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    order_index: int


class PathwayResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    items: List[PathwayItemResponse]
