import uuid
from typing import List, Optional
from pydantic import BaseModel, Field


class PathwayItemSchema(BaseModel):
    product_id: uuid.UUID
    order_index: Optional[int] = None


class PathwayCreate(BaseModel):
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
