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
    level_id: uuid.UUID
    duration: str
    cover: Optional[str] = None
    short_video: Optional[str] = None

    created_by: Optional[uuid.UUID] = None

    # Book Video details
    author_name: str
    author_bio: Optional[str] = None
    expected_time_completion: Optional[int] = None

    # Relations
    videos: Optional[List[BookVideoSchema]] = Field(default=None)
    skills: Optional[List[uuid.UUID]] = Field(default=None)
    objectives: Optional[List[uuid.UUID]] = Field(default=None)

