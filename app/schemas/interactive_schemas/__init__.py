# Import from new separated files
from .request_schemas import (
    # Enums
    VisualTypeEnum,
    ChartTypeEnum,
    
    # Course request schemas
    InteractiveCourseCreateSchema,
    InteractiveCourseUpdateSchema,
    InteractiveChapterDetails,
    
    # Chapter request schemas
    InteractiveChapterCreateSchema,
    InteractiveChapterUpdateSchema,
    
    # Video request schemas
    InteractiveVideoCreateSchema,
    InteractiveVideoUpdateSchema,
    
    # Paragraph request schemas
    InteractiveParagraphCreateSchema,
    
    # Word and keyword request schemas
    InteractiveWordCreateSchema,
    InteractiveKeywordCreateSchema,
    InteractiveKeywordUpdateSchema,
    VideoKeywordTypeStyleCreateSchema,
    
    # Visual data request schemas
    TableDataCreateSchema,
    ChartDataCreateSchema,
    ImageDataCreateSchema,
    VisualDataCreateSchema,
    VisualDataUpdateSchema,
    VideoKeywordTypeStyleUpdateSchema
)

from .response_schemas import (
    # Course response schemas
    InteractiveCourseResponse,
    InteractiveCourseDetailSchema,
    
    # Chapter response schemas
    InteractiveChapterResponse,
    
    # Video response schemas
    InteractiveVideoResponse,
    InteractiveVideoDetails,
    
    # Paragraph response schemas
    InteractiveParagraphResponse,
    
    # Word and keyword response schemas
    InteractiveWordResponse,
    InteractiveKeywordResponse,
    
    # Visual data response schemas
    TableDataResponse,
    ChartDataResponse,
    ImageDataResponse,
    VisualDataResponse,
)

# Keep existing imports for backward compatibility
from .interactive_paragraph_schema import (
    InteractiveParagraphSchema,
    InteractiveParagraphCreateSchema as InteractiveParagraphCreateSchemaOld,
    InteractiveWordSchema,
    InteractiveWordResponse,
    InteractiveWordCreateSchema as InteractiveWordCreateSchemaOld,
    WordTypeResponse,
    WordTypeCreateSchema,
    InteractiveParagraphWithDetailsResponse,
)
from .interactive_keyword_schema import (
    InteractiveKeyWordSchema,
    InteractiveKeyWordResponse,
    InteractiveKeyWordCreateSchema,
    KeyWordTypeResponse,
    KeyWordTypeCreateSchema,
    VideoKeywordTypeStyleSchema,
    VideoKeywordTypeStyleResponse,
    VideoKeywordTypeStyleCreateSchema,
    KeyWordTypeWithStylesResponse,
)
from .interactive_visual_schema import (
    VisualItemSchema,
    VisualItemResponse,
    VisualItemCreateSchema,
    VisualTypeResponse,
    VisualTypeCreateSchema,
    TableDataSchema,
    TableDataResponse,
    TableDataCreateSchema as TableDataCreateSchemaOld,
    ChartDataSchema,
    ChartDataResponse,
    ChartDataCreateSchema as ChartDataCreateSchemaOld,
    ChartTypeResponse,
    ChartTypeCreateSchema,
    ImageSchema,
    ImageResponse,
    ImageCreateSchema,
)

__all__ = [
    # Enums
    "VisualTypeEnum",
    "ChartTypeEnum",
    
    # Course schemas
    "InteractiveCourseCreateSchema",
    "InteractiveCourseUpdateSchema",
    "InteractiveCourseResponse",
    "InteractiveCourseDetailSchema",
    "InteractiveChapterDetails",
    
    # Chapter schemas
    "InteractiveChapterCreateSchema",
    "InteractiveChapterUpdateSchema",
    "InteractiveChapterResponse",
    
    # Video schemas
    "InteractiveVideoCreateSchema",
    "InteractiveVideoUpdateSchema",
    "InteractiveVideoResponse",
    "InteractiveVideoDetails",
    
    # Paragraph schemas
    "InteractiveParagraphCreateSchema",
    "InteractiveParagraphResponse",
    "InteractiveParagraphSchema",
    "InteractiveParagraphWithDetailsResponse",
    
    # Word and keyword schemas
    "InteractiveWordCreateSchema",
    "InteractiveWordResponse",
    "InteractiveWordSchema",
    "InteractiveKeywordCreateSchema",
    "InteractiveKeywordUpdateSchema",
    "InteractiveKeywordResponse",
    "VideoKeywordTypeStyleCreateSchema",
    "InteractiveKeyWordSchema",
    "InteractiveKeyWordResponse",
    "InteractiveKeyWordCreateSchema",
    "WordTypeResponse",
    "WordTypeCreateSchema",
    "KeyWordTypeResponse",
    "KeyWordTypeCreateSchema",
    "VideoKeywordTypeStyleSchema",
    "VideoKeywordTypeStyleResponse",
    "VideoKeywordTypeStyleCreateSchema",
    "KeyWordTypeWithStylesResponse",
    
    # Visual data schemas
    "TableDataCreateSchema",
    "ChartDataCreateSchema",
    "ImageDataCreateSchema",
    "VisualDataCreateSchema",
    "VisualDataUpdateSchema",
    "TableDataResponse",
    "ChartDataResponse",
    "ImageDataResponse",
    "VisualDataResponse",
    "VisualItemSchema",
    "VisualItemResponse",
    "VisualItemCreateSchema",
    "VisualTypeResponse",
    "VisualTypeCreateSchema",
    "TableDataSchema",
    "ChartDataSchema",
    "ChartTypeResponse",
    "ChartTypeCreateSchema",
    "ImageSchema",
    "ImageResponse",
    "ImageCreateSchema",
]