import uuid
from typing import List, Optional
from pydantic import BaseModel, Field


class VideoDetails(BaseModel):
    title: str
    url: str
    video_duration: Optional[str] = Field(default=None)
    view_index: Optional[int] = Field(default=None)
    quiz_id: Optional[uuid.UUID] = Field(default=None)


class ChapterDetails(BaseModel):
    title: str
    description: str
    videos: List[VideoDetails]
    quiz_id: Optional[uuid.UUID] = Field(default=None)


class CourseDetailSchema(BaseModel):
    product_type_id: uuid.UUID
    product_category_id: uuid.UUID
    created_by: Optional[uuid.UUID]
    level_id: Optional[uuid.UUID] = Field(default=None)
    title: str
    description: str
    language: str
    duration: str
    chapters: List[ChapterDetails]
    cover: Optional[str] = Field(default=None)
    short_video: Optional[str] = Field(default=None)

    # optional extras
    video_count: Optional[int] = Field(default=None)
    students_count: Optional[int] = Field(default=None)
    pre_assessment_id: Optional[uuid.UUID] = Field(default=None)
    final_exam_id: Optional[uuid.UUID] = Field(default=None)
    certificate_included: Optional[bool] = Field(default=False)
    view_index: Optional[int] = Field(default=None)

    # relations
    skills: Optional[List[uuid.UUID]] = Field(default=None)
    objectives: Optional[List[uuid.UUID]] = Field(default=None)
    instructors: Optional[List[uuid.UUID]] = Field(default=None)
