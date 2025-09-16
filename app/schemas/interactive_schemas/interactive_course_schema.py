import uuid
from typing import List, Optional
from pydantic import BaseModel, Field


class InteractiveVideoDetails(BaseModel):
    title: str
    url: str
    video_duration: str
    view_index: Optional[int] = Field(default=None)
    quiz_id: Optional[uuid.UUID] = Field(default=None)


class InteractiveChapterDetails(BaseModel):
    title: str
    description: str
    about: Optional[str] = Field(default=None)
    view_index: int
    # videos: List[InteractiveVideoDetails]
    quiz_id: Optional[uuid.UUID] = Field(default=None)


class InteractiveCourseCreateSchema(BaseModel):
    # Product fields (required for creating the product)
    # type_id: uuid.UUID
    category_id: uuid.UUID
    created_by: Optional[uuid.UUID] = Field(default=None)
    level_id: Optional[uuid.UUID] = Field(default=None)
    title: str
    description: str
    language: str
    duration: str
    cover: Optional[str] = Field(default=None)
    short_video: Optional[str] = Field(default=None)
    
    # Interactive course specific fields
    pre_assessment_id: Optional[uuid.UUID] = Field(default=None)
    final_exam_id: Optional[uuid.UUID] = Field(default=None)
    
    # Related data
    skills: Optional[List[uuid.UUID]] = Field(default=None)
    objectives: Optional[List[uuid.UUID]] = Field(default=None)
    chapters: Optional[List[InteractiveChapterDetails]] = Field(default=None)


class InteractiveCourseUpdateSchema(BaseModel):
    # Product fields (optional for updates)
    category_id: Optional[uuid.UUID] = Field(default=None)
    level_id: Optional[uuid.UUID] = Field(default=None)
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default=None)
    duration: Optional[str] = Field(default=None)
    cover: Optional[str] = Field(default=None)
    short_video: Optional[str] = Field(default=None)
    
    # Interactive course specific fields
    pre_assessment_id: Optional[uuid.UUID] = Field(default=None)
    final_exam_id: Optional[uuid.UUID] = Field(default=None)
    
    # Related data
    skills: Optional[List[uuid.UUID]] = Field(default=None)
    objectives: Optional[List[uuid.UUID]] = Field(default=None)


class InteractiveCourseDetailSchema(BaseModel):
    product_type_id: uuid.UUID
    product_category_id: uuid.UUID
    created_by: Optional[uuid.UUID]
    level_id: Optional[uuid.UUID] = Field(default=None)
    title: str
    description: str
    language: str
    duration: str
    chapters: List[InteractiveChapterDetails]
    cover: Optional[str] = Field(default=None)
    short_video: Optional[str] = Field(default=None)

    video_count: Optional[int] = Field(default=None)
    students_count: Optional[int] = Field(default=None)
    pre_assessment_id: Optional[uuid.UUID] = Field(default=None)
    final_exam_id: Optional[uuid.UUID] = Field(default=None)
    certificate_included: Optional[bool] = Field(default=False)
    view_index: Optional[int] = Field(default=None)

    skills: Optional[List[uuid.UUID]] = Field(default=None)
    objectives: Optional[List[uuid.UUID]] = Field(default=None)


class InteractiveCourseResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    pre_assessment_id: Optional[uuid.UUID] = Field(default=None)
    final_exam_id: Optional[uuid.UUID] = Field(default=None)
    chapters: List[InteractiveChapterDetails]

    class Config:
        from_attributes = True


class InteractiveChapterResponse(BaseModel):
    id: uuid.UUID
    course_id: uuid.UUID
    quiz_id: Optional[uuid.UUID] = Field(default=None)
    title: str
    description: str
    about: Optional[str] = Field(default=None)
    view_index: int
    videos: List[InteractiveVideoDetails]

    class Config:
        from_attributes = True


class InteractiveVideoResponse(BaseModel):
    id: uuid.UUID
    chapter_id: uuid.UUID
    quiz_id: Optional[uuid.UUID] = Field(default=None)
    title: str
    url: str
    video_duration: str
    view_index: int

    class Config:
        from_attributes = True


class InteractiveVideoCreateSchema(BaseModel):
    chapter_id: uuid.UUID
    quiz_id: Optional[uuid.UUID] = Field(default=None)
    title: str
    url: str
    video_duration: str
    view_index: int


class InteractiveChapterCreateSchema(BaseModel):
    course_id: uuid.UUID
    quiz_id: Optional[uuid.UUID] = Field(default=None)
    title: str
    description: str
    about: Optional[str] = Field(default=None)
    view_index: int


class InteractiveChapterUpdateSchema(BaseModel):
    quiz_id: Optional[uuid.UUID] = Field(default=None)
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    about: Optional[str] = Field(default=None)
    view_index: Optional[int] = Field(default=None)


