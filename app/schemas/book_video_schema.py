import uuid
from typing import List, Optional
from pydantic import BaseModel, Field, condecimal


# ---------------------------
# Video schema
# ---------------------------
class BookVideoSchema(BaseModel):
    video_name: str
    video_duration: str
    url: str
    view_index: Optional[int] = Field(default=None)


# ---------------------------
# Book Video Create schema
# ---------------------------
class BookVideoCreate(BaseModel):
    # Product fields
    product_type_id: uuid.UUID
    product_category_id: uuid.UUID
    title: str
    description: str
    language: str
    level: str
    duration: int

    # Book Video details
    author_name: str
    cover_path: Optional[str] = None
    price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    total_videos: Optional[int] = None
    total_hours: Optional[int] = None
    url: Optional[str] = None
    expected_time_completion: Optional[int] = None

    # Relations
    videos: Optional[List[BookVideoSchema]] = Field(default=None)
    skills: Optional[List[uuid.UUID]] = Field(default=None)
    objectives: Optional[List[uuid.UUID]] = Field(default=None)

