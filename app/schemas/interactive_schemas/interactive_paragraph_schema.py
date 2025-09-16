import uuid
from typing import List, Optional
from pydantic import BaseModel, Field


class InteractiveWordSchema(BaseModel):
    word: str
    start_time: float
    end_time: float
    type_id: uuid.UUID


class InteractiveWordResponse(BaseModel):
    id: uuid.UUID
    paragraph_id: uuid.UUID
    type_id: uuid.UUID
    word: str
    start_time: float
    end_time: float

    class Config:
        from_attributes = True


class WordTypeResponse(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        from_attributes = True


class WordTypeCreateSchema(BaseModel):
    name: str


class InteractiveParagraphSchema(BaseModel):
    video_id: uuid.UUID
    view_index: int
    paragraph_text: str
    start_time: float
    end_time: float
    words: Optional[List[InteractiveWordSchema]] = Field(default=None)


class InteractiveParagraphResponse(BaseModel):
    id: uuid.UUID
    video_id: uuid.UUID
    view_index: int
    paragraph_text: str
    start_time: float
    end_time: float
    paragraph_words: Optional[List[InteractiveWordResponse]] = Field(default=None)

    class Config:
        from_attributes = True


class InteractiveParagraphCreateSchema(BaseModel):
    video_id: uuid.UUID
    view_index: int
    paragraph_text: str
    start_time: float
    end_time: float


class InteractiveWordCreateSchema(BaseModel):
    paragraph_id: uuid.UUID
    type_id: uuid.UUID
    word: str
    start_time: float
    end_time: float


class InteractiveParagraphWithDetailsResponse(BaseModel):
    id: uuid.UUID
    video_id: uuid.UUID
    view_index: int
    paragraph_text: str
    start_time: float
    end_time: float
    paragraph_words: Optional[List[InteractiveWordResponse]] = Field(default=None)

    class Config:
        from_attributes = True