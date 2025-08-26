from pydantic import BaseModel


class InstructorBase(BaseModel):
    name: str
    title: str | None = None
    bio: str | None = None
    linkedin: str | None = None
    education: str | None = None
    rating: float | None = None
    review_count: int = 0
    courses_count: int = 0
    students_count: int = 0
    is_top_rated: bool = False
    is_featured: bool = False
    is_expert: bool = False
    is_new: bool = False
