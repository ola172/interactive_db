import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

# Import ImageTypeEnum from visual models
from app.models.interactive_models.visual_models import ImageTypeEnum
from app.models.interactive_models.assist_image_model import AssistImageTypeEnum


class VisualTypeEnum(str, Enum):
    CHART = "chart"
    IMAGE = "image"
    TABLE = "table"


class ChartTypeEnum(str, Enum):
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    RADAR = "radar"


# Word and Keyword Request Schemas
class InteractiveWordCreateSchema(BaseModel):
    word_type_id: uuid.UUID  # Reference to WordType by ID
    word: str
    start_time: float
    end_time: float


class KeyWordTypeCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None


class WordTypeCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None


class InteractiveKeywordCreateSchema(BaseModel):
    keyword_type_id: uuid.UUID
    word: str


class InteractiveKeywordUpdateSchema(BaseModel):
    word: Optional[str] = Field(default=None)
    keyword_type_id: Optional[uuid.UUID] = Field(default=None)


class KeyWordTypeUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


class WordTypeUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


class VisualTypeCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None


class VisualTypeUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


class ChartTypeCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None


class ChartTypeUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


# Keyword Type Style Schema for Video
class VideoKeywordTypeStyleUpdateSchema(BaseModel):
    color_light: Optional[str] = Field(default=None)
    color_dark: Optional[str] = Field(default=None)
    shadow_light: Optional[str] = Field(default=None)
    shadow_dark: Optional[str] = Field(default=None)
    size: Optional[int] = Field(default=None)


# Visual Data Request Schemas
class TableDataCreateSchema(BaseModel):
    headers: List[str]
    rows: List[List[str]]
    title: str
    caption: Optional[str]


class ChartDataCreateSchema(BaseModel):
    chart_type_id: uuid.UUID  # Reference to ChartType by ID
    labels: List[str]  # Chart labels
    data: List[float]  # Chart data as list of floats or tuples
    title: str  # Chart title


class ImageDataCreateSchema(BaseModel):
    image_type: ImageTypeEnum = Field(..., description="Type of image (2D or 3D)")
    url: str
    title: str = Field(..., description="Image title")
    alt_text: Optional[str] = Field(default=None)


class VisualDataCreateSchema(BaseModel):
    visual_type_id: uuid.UUID
    start_time: float
    table_data: Optional[TableDataCreateSchema] = Field(default=None)
    chart_data: Optional[ChartDataCreateSchema] = Field(default=None)
    image_data: Optional[ImageDataCreateSchema] = Field(default=None)
    assist_image_id: Optional[uuid.UUID] = Field(default=None, description="ID of existing assist image to link to this visual item")


class VisualDataUpdateSchema(BaseModel):
    visual_type_id: uuid.UUID
    start_time: Optional[float] = Field(default=None)
    table_data: Optional[TableDataCreateSchema] = Field(default=None)
    chart_data: Optional[ChartDataCreateSchema] = Field(default=None)
    image_data: Optional[ImageDataCreateSchema] = Field(default=None)
    assist_image_id: Optional[uuid.UUID] = Field(default=None, description="ID of existing assist image to link to this visual item")


# Paragraph Request Schemas
class InteractiveParagraphCreateSchema(BaseModel):
    view_index: int
    paragraph_text: str
    start_time: float
    end_time: float
    words: List[InteractiveWordCreateSchema] = Field()
    keywords: List[InteractiveKeywordCreateSchema] = Field(default=[])
    visual_data: Optional[VisualDataCreateSchema] = Field(default=None)


# Video Request Schemas
class InteractiveVideoCreateSchema(BaseModel):
    chapter_id: uuid.UUID
    quiz_id: Optional[uuid.UUID] = Field(default=None)
    title: str
    url: str
    video_duration: str
    view_index: int
    paragraphs: List[InteractiveParagraphCreateSchema] = Field(
        description="All paragraphs data is required"
    )


class InteractiveVideoUpdateSchema(BaseModel):
    quiz_id: Optional[uuid.UUID] = Field(default=None)
    title: Optional[str] = Field(default=None)
    url: Optional[str] = Field(default=None)
    video_duration: Optional[str] = Field(default=None)
    view_index: Optional[int] = Field(default=None)


# Chapter Request Schemas
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


# Course Request Schemas
class InteractiveChapterDetails(BaseModel):
    title: str
    description: str
    about: Optional[str] = Field(default=None)
    view_index: int
    quiz_id: Optional[uuid.UUID] = Field(default=None)


class InteractiveCourseCreateSchema(BaseModel):
    # Product fields (required for creating the product)
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


class FileCreateSchema(BaseModel):
    video_id: Optional[uuid.UUID] = Field(default=None)
    file_type_id: uuid.UUID


class FileUpdateSchema(BaseModel):
    file_name: Optional[str] = Field(default=None)
    video_id: Optional[uuid.UUID] = Field(default=None)
    file_type_id: Optional[uuid.UUID] = Field(default=None)
    bucket_name: Optional[str] = Field(default=None)
    storage_path: Optional[str] = Field(default=None)
    file_url: Optional[str] = Field(default=None)


class ImageCreateSchema(BaseModel):
    file_id: uuid.UUID
    image_title: str
    proposed_image_type: AssistImageTypeEnum
    is_protected: bool = False
    searched_image_url: Optional[str] = Field(default=None)
    image_3d_url: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


class ImageUpdateSchema(BaseModel):
    image_title: Optional[str] = Field(default=None)
    proposed_image_type: Optional[AssistImageTypeEnum] = Field(default=None)
    is_protected: Optional[bool] = Field(default=None)
    original_image_url: Optional[str] = Field(default=None)
    searched_image_url: Optional[str] = Field(default=None)
    image_3d_url: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


class FileTypeCreateSchema(BaseModel):
    name: str
    description: Optional[str] = Field(default=None)


# Video Keyword Style Schema
class VideoKeywordStyleCreateSchema(BaseModel):
    keyword_type_id: uuid.UUID = Field(..., description="Keyword type ID")
    color_light: str = Field(..., min_length=1, max_length=50, description="Color for light theme (e.g., #000000)")
    color_dark: str = Field(..., min_length=1, max_length=50, description="Color for dark theme (e.g., #FFFFFF)")
    shadow_light: Optional[str] = Field(default=None, max_length=50, description="Shadow for light theme")
    shadow_dark: Optional[str] = Field(default=None, max_length=50, description="Shadow for dark theme")
    size: int = Field(default=14, ge=8, le=72, description="Font size")


class VideoKeywordStyleUpdateSchema(BaseModel):
    keyword_type_id: uuid.UUID = Field(..., description="Keyword type ID to update")
    color_light: Optional[str] = Field(default=None, min_length=1, max_length=50, description="Color for light theme")
    color_dark: Optional[str] = Field(default=None, min_length=1, max_length=50, description="Color for dark theme")
    shadow_light: Optional[str] = Field(default=None, max_length=50, description="Shadow for light theme")
    shadow_dark: Optional[str] = Field(default=None, max_length=50, description="Shadow for dark theme")
    size: Optional[int] = Field(default=None, ge=8, le=72, description="Font size")


# Video Upload Schema with all fields from InteractiveVideoCreateSchema
class InteractiveVideoUploadSchema(BaseModel):
    # Core video fields (same as InteractiveVideoCreateSchema)
    chapter_id: uuid.UUID = Field(..., description="Chapter ID this video belongs to")
    quiz_id: Optional[uuid.UUID] = Field(default=None, description="Optional quiz ID")
    title: str = Field(..., min_length=1, max_length=255, description="Video title")
    video_duration: str = Field(..., description="Video duration (e.g., '10:30')")
    view_index: int = Field(..., ge=0, description="Display order index")
    
    # Paragraphs data (same as create schema)
    paragraphs: List[InteractiveParagraphCreateSchema] = Field(
        description="All paragraphs data is required"
    )
    
    # Additional upload-specific fields
    asset_file_id: Optional[uuid.UUID]= Field(default=None, description="Asset file ID to update with video reference")
    keyword_styles: List[VideoKeywordStyleCreateSchema] = Field(default=[], description="Keyword styles for this video")
